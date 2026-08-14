const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { DatabaseSync } = require('node:sqlite');
const { hashPassword, verifyPassword, newSessionToken, tokenDigest } = require('./auth');

class ForbiddenError extends Error {
  constructor(message = 'Forbidden') {
    super(message);
    this.name = 'ForbiddenError';
    this.statusCode = 403;
  }
}

class ValidationError extends Error {
  constructor(message = 'Invalid input') {
    super(message);
    this.name = 'ValidationError';
    this.statusCode = 400;
  }
}

function nowIso() {
  return new Date().toISOString();
}

function plusHours(hours) {
  return new Date(Date.now() + hours * 3600_000).toISOString();
}

class RelayStore {
  constructor({ filename = process.env.RELAYOPS_DB || path.join(process.cwd(), '.relayops', 'relayops.sqlite'), storageRoot = process.env.RELAYOPS_STORAGE || path.join(process.cwd(), '.relayops', 'files') } = {}) {
    this.filename = filename;
    this.storageRoot = storageRoot;
    if (filename !== ':memory:') fs.mkdirSync(path.dirname(filename), { recursive: true });
    fs.mkdirSync(storageRoot, { recursive: true });
    this.db = new DatabaseSync(filename);
    this.permissionCache = new Map();
    this.init();
  }

  init() {
    this.db.exec(`
      PRAGMA foreign_keys = ON;
      CREATE TABLE IF NOT EXISTS organization (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS user_account (
        id TEXT PRIMARY KEY,
        email TEXT NOT NULL UNIQUE,
        display_name TEXT NOT NULL,
        password_salt TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        platform_role TEXT
      );
      CREATE TABLE IF NOT EXISTS membership (
        user_id TEXT NOT NULL,
        tenant_id TEXT NOT NULL,
        role TEXT NOT NULL,
        auth_version INTEGER NOT NULL DEFAULT 1,
        PRIMARY KEY(user_id, tenant_id),
        FOREIGN KEY(user_id) REFERENCES user_account(id),
        FOREIGN KEY(tenant_id) REFERENCES organization(id)
      );
      CREATE TABLE IF NOT EXISTS session (
        token_hash TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        tenant_id TEXT,
        expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES user_account(id)
      );
      CREATE TABLE IF NOT EXISTS customer (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        created_at TEXT NOT NULL,
        UNIQUE(tenant_id, email),
        FOREIGN KEY(tenant_id) REFERENCES organization(id)
      );
      CREATE INDEX IF NOT EXISTS customer_tenant_name_idx ON customer(tenant_id, name);
      CREATE TABLE IF NOT EXISTS work_order (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        customer_id TEXT NOT NULL,
        title TEXT NOT NULL,
        status TEXT NOT NULL,
        priority TEXT NOT NULL,
        assigned_user_id TEXT,
        version INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES organization(id),
        FOREIGN KEY(customer_id) REFERENCES customer(id)
      );
      CREATE INDEX IF NOT EXISTS work_order_tenant_status_idx ON work_order(tenant_id, status, updated_at);
      CREATE TABLE IF NOT EXISTS attachment (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        work_order_id TEXT NOT NULL,
        name TEXT NOT NULL,
        relative_path TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES organization(id),
        FOREIGN KEY(work_order_id) REFERENCES work_order(id)
      );
      CREATE TABLE IF NOT EXISTS notification (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        user_id TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL,
        read_at TEXT,
        FOREIGN KEY(tenant_id) REFERENCES organization(id),
        FOREIGN KEY(user_id) REFERENCES user_account(id)
      );
      CREATE TABLE IF NOT EXISTS job (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        kind TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        status TEXT NOT NULL,
        attempts INTEGER NOT NULL DEFAULT 0,
        next_run_at TEXT NOT NULL,
        idempotency_key TEXT NOT NULL UNIQUE,
        last_error TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );
      CREATE INDEX IF NOT EXISTS job_ready_idx ON job(status, next_run_at);
      CREATE TABLE IF NOT EXISTS billing_event (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        provider_event_id TEXT NOT NULL UNIQUE,
        provider_version INTEGER NOT NULL,
        event_type TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        applied INTEGER NOT NULL,
        created_at TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS entitlement (
        tenant_id TEXT PRIMARY KEY,
        plan TEXT NOT NULL,
        status TEXT NOT NULL,
        provider_version INTEGER NOT NULL DEFAULT 0,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(tenant_id) REFERENCES organization(id)
      );
      CREATE TABLE IF NOT EXISTS audit_log (
        id TEXT PRIMARY KEY,
        tenant_id TEXT NOT NULL,
        actor_user_id TEXT NOT NULL,
        action TEXT NOT NULL,
        target_type TEXT NOT NULL,
        target_id TEXT,
        detail_json TEXT NOT NULL,
        created_at TEXT NOT NULL
      );
      CREATE INDEX IF NOT EXISTS audit_tenant_created_idx ON audit_log(tenant_id, created_at);
      CREATE TABLE IF NOT EXISTS import_row (
        tenant_id TEXT NOT NULL,
        batch_key TEXT NOT NULL,
        row_number INTEGER NOT NULL,
        row_key TEXT NOT NULL,
        status TEXT NOT NULL,
        error TEXT,
        customer_id TEXT,
        PRIMARY KEY(tenant_id, batch_key, row_number)
      );
    `);
    this.seed();
  }

  seed() {
    const organizations = [
      ['northline', 'Northline Facilities'],
      ['harbor', 'Harbor Service Group'],
    ];
    const insertOrg = this.db.prepare('INSERT OR IGNORE INTO organization(id, name) VALUES (?, ?)');
    const insertEntitlement = this.db.prepare('INSERT OR IGNORE INTO entitlement(tenant_id, plan, status, provider_version, updated_at) VALUES (?, ?, ?, ?, ?)');
    for (const [id, name] of organizations) {
      insertOrg.run(id, name);
      insertEntitlement.run(id, 'operations-pro', 'active', 1, nowIso());
    }

    const users = [
      ['u-north-manager', 'manager@northline.test', 'Maya Chen', 'manager', 'northline'],
      ['u-north-dispatch', 'dispatch@northline.test', 'Owen Brooks', 'dispatcher', 'northline'],
      ['u-north-tech', 'tech@northline.test', 'Lina Park', 'technician', 'northline'],
      ['u-north-billing', 'billing@northline.test', 'Samira Holt', 'billing', 'northline'],
      ['u-harbor-manager', 'manager@harbor.test', 'Dario Mendes', 'manager', 'harbor'],
    ];
    const insertUser = this.db.prepare('INSERT OR IGNORE INTO user_account(id, email, display_name, password_salt, password_hash, platform_role) VALUES (?, ?, ?, ?, ?, NULL)');
    const insertMembership = this.db.prepare('INSERT OR IGNORE INTO membership(user_id, tenant_id, role, auth_version) VALUES (?, ?, ?, 1)');
    for (const [id, email, name, role, tenantId] of users) {
      const credential = hashPassword('relayops-demo');
      insertUser.run(id, email, name, credential.salt, credential.hash);
      insertMembership.run(id, tenantId, role);
    }
    const supportCredential = hashPassword('relayops-support');
    this.db.prepare('INSERT OR IGNORE INTO user_account(id, email, display_name, password_salt, password_hash, platform_role) VALUES (?, ?, ?, ?, ?, ?)')
      .run('u-platform-support', 'support@relayops.test', 'RelayOps Support', supportCredential.salt, supportCredential.hash, 'support');

    const customerCount = this.db.prepare('SELECT COUNT(*) AS n FROM customer').get().n;
    if (Number(customerCount) === 0) {
      const addCustomer = this.db.prepare('INSERT INTO customer(id, tenant_id, name, email, phone, created_at) VALUES (?, ?, ?, ?, ?, ?)');
      addCustomer.run('c-north-1', 'northline', 'Atlas Dental Group', 'ops@atlasdental.test', '+1 415 555 0101', nowIso());
      addCustomer.run('c-north-2', 'northline', 'Juniper Market', 'facilities@juniper.test', '+1 415 555 0102', nowIso());
      addCustomer.run('c-harbor-1', 'harbor', 'Beacon Kitchens', 'ops@beacon.test', '+1 206 555 0144', nowIso());
      const addOrder = this.db.prepare('INSERT INTO work_order(id, tenant_id, customer_id, title, status, priority, assigned_user_id, version, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)');
      addOrder.run('wo-north-1', 'northline', 'c-north-1', 'Replace compressor relay', 'scheduled', 'high', 'u-north-tech', nowIso(), nowIso());
      addOrder.run('wo-north-2', 'northline', 'c-north-2', 'Quarterly refrigeration inspection', 'new', 'normal', null, nowIso(), nowIso());
      addOrder.run('wo-harbor-1', 'harbor', 'c-harbor-1', 'Walk-in cooler diagnostics', 'in_progress', 'urgent', null, nowIso(), nowIso());
    }
  }

  close() {
    this.db.close();
  }

  login(email, password, requestedTenant = null) {
    const user = this.db.prepare('SELECT * FROM user_account WHERE email = ?').get(String(email).trim().toLowerCase());
    if (!user || !verifyPassword(password, user.password_salt, user.password_hash)) return null;
    let tenantId = null;
    let role = user.platform_role || null;
    if (!user.platform_role) {
      const memberships = this.db.prepare('SELECT tenant_id, role FROM membership WHERE user_id = ? ORDER BY tenant_id').all(user.id);
      const membership = requestedTenant
        ? memberships.find((row) => row.tenant_id === requestedTenant)
        : memberships[0];
      if (!membership) return null;
      tenantId = membership.tenant_id;
      role = membership.role;
    }
    const token = newSessionToken();
    this.db.prepare('INSERT INTO session(token_hash, user_id, tenant_id, expires_at, created_at) VALUES (?, ?, ?, ?, ?)')
      .run(tokenDigest(token), user.id, tenantId, plusHours(12), nowIso());
    return {
      token,
      actor: { userId: user.id, email: user.email, displayName: user.display_name, tenantId, role, platformRole: user.platform_role || null },
    };
  }

  logout(token) {
    this.db.prepare('DELETE FROM session WHERE token_hash = ?').run(tokenDigest(token));
  }

  actorFromToken(token) {
    if (!token) return null;
    const row = this.db.prepare(`
      SELECT s.user_id, s.tenant_id, s.expires_at, u.email, u.display_name, u.platform_role
      FROM session s JOIN user_account u ON u.id = s.user_id
      WHERE s.token_hash = ?
    `).get(tokenDigest(token));
    if (!row || row.expires_at <= nowIso()) return null;
    if (row.platform_role === 'support') {
      return { userId: row.user_id, email: row.email, displayName: row.display_name, tenantId: null, role: 'support', platformRole: 'support' };
    }
    const membership = this.db.prepare('SELECT role FROM membership WHERE user_id = ? AND tenant_id = ?').get(row.user_id, row.tenant_id);
    if (!membership) return null;
    return { userId: row.user_id, email: row.email, displayName: row.display_name, tenantId: row.tenant_id, role: membership.role, platformRole: null };
  }

  switchTenant(actor, tenantId) {
    if (!actor || actor.platformRole) throw new ForbiddenError();
    const membership = this.db.prepare('SELECT role FROM membership WHERE user_id = ? AND tenant_id = ?').get(actor.userId, tenantId);
    if (!membership) throw new ForbiddenError('Organization membership required');
    return { ...actor, tenantId, role: membership.role };
  }

  permissionSnapshot(actor) {
    if (!actor || !actor.tenantId || actor.platformRole) throw new ForbiddenError('Tenant session required');
    const membership = this.db.prepare('SELECT role, auth_version FROM membership WHERE user_id = ? AND tenant_id = ?').get(actor.userId, actor.tenantId);
    if (!membership) throw new ForbiddenError('Membership revoked');
    const entitlement = this.db.prepare('SELECT plan, status, provider_version FROM entitlement WHERE tenant_id = ?').get(actor.tenantId);
    const key = `${actor.tenantId}:${actor.userId}:${membership.auth_version}:${entitlement?.provider_version || 0}:${entitlement?.status || 'none'}`;
    if (!this.permissionCache.has(key)) {
      this.permissionCache.set(key, { role: membership.role, authVersion: membership.auth_version, plan: entitlement?.plan || null, entitlementStatus: entitlement?.status || 'inactive' });
    }
    return this.permissionCache.get(key);
  }

  authorize(actor, roles = []) {
    const snapshot = this.permissionSnapshot(actor);
    if (roles.length && !roles.includes(snapshot.role)) throw new ForbiddenError('Role does not permit this action');
    if (snapshot.entitlementStatus !== 'active') throw new ForbiddenError('Subscription entitlement is not active');
    return snapshot;
  }

  revokeMembership(userId, tenantId) {
    this.db.prepare('DELETE FROM membership WHERE user_id = ? AND tenant_id = ?').run(userId, tenantId);
    this.permissionCache.clear();
  }

  organization(actor) {
    this.authorize(actor);
    return this.db.prepare('SELECT id, name FROM organization WHERE id = ?').get(actor.tenantId);
  }

  listCustomers(actor, query = '') {
    this.authorize(actor);
    const q = `%${String(query).trim()}%`;
    return this.db.prepare('SELECT id, name, email, phone, created_at FROM customer WHERE tenant_id = ? AND (name LIKE ? OR email LIKE ?) ORDER BY name').all(actor.tenantId, q, q);
  }

  getCustomer(actor, customerId) {
    this.authorize(actor);
    const row = this.db.prepare('SELECT id, name, email, phone, created_at FROM customer WHERE tenant_id = ? AND id = ?').get(actor.tenantId, customerId);
    if (!row) throw new ForbiddenError('Customer not available in active organization');
    return row;
  }

  createCustomer(actor, input) {
    this.authorize(actor, ['manager', 'dispatcher']);
    const name = String(input.name || '').trim();
    const email = String(input.email || '').trim().toLowerCase();
    if (!name || !email.includes('@')) throw new ValidationError('Name and valid email are required');
    const id = crypto.randomUUID();
    this.db.prepare('INSERT INTO customer(id, tenant_id, name, email, phone, created_at) VALUES (?, ?, ?, ?, ?, ?)')
      .run(id, actor.tenantId, name, email, String(input.phone || '').trim() || null, nowIso());
    this.audit(actor, 'customer.created', 'customer', id, { email });
    return this.getCustomer(actor, id);
  }

  listWorkOrders(actor, { status = '', query = '' } = {}) {
    this.authorize(actor);
    const q = `%${String(query).trim()}%`;
    const statusFilter = String(status || '').trim();
    return this.db.prepare(`
      SELECT w.id, w.title, w.status, w.priority, w.assigned_user_id, w.version, w.updated_at,
             c.name AS customer_name, c.id AS customer_id
      FROM work_order w JOIN customer c ON c.id = w.customer_id AND c.tenant_id = w.tenant_id
      WHERE w.tenant_id = ? AND (? = '' OR w.status = ?) AND (w.title LIKE ? OR c.name LIKE ?)
      ORDER BY CASE w.priority WHEN 'urgent' THEN 0 WHEN 'high' THEN 1 ELSE 2 END, w.updated_at DESC
    `).all(actor.tenantId, statusFilter, statusFilter, q, q);
  }

  getWorkOrder(actor, workOrderId) {
    this.authorize(actor);
    const row = this.db.prepare(`
      SELECT w.*, c.name AS customer_name
      FROM work_order w JOIN customer c ON c.id = w.customer_id AND c.tenant_id = w.tenant_id
      WHERE w.tenant_id = ? AND w.id = ?
    `).get(actor.tenantId, workOrderId);
    if (!row) throw new ForbiddenError('Work order not available in active organization');
    return row;
  }

  createWorkOrder(actor, input) {
    this.authorize(actor, ['manager', 'dispatcher']);
    const customer = this.getCustomer(actor, input.customerId);
    const title = String(input.title || '').trim();
    if (!title) throw new ValidationError('Title is required');
    const priority = ['normal', 'high', 'urgent'].includes(input.priority) ? input.priority : 'normal';
    const id = crypto.randomUUID();
    const at = nowIso();
    this.db.prepare(`
      INSERT INTO work_order(id, tenant_id, customer_id, title, status, priority, assigned_user_id, version, created_at, updated_at)
      VALUES (?, ?, ?, ?, 'new', ?, NULL, 1, ?, ?)
    `).run(id, actor.tenantId, customer.id, title, priority, at, at);
    this.audit(actor, 'work_order.created', 'work_order', id, { priority });
    return this.getWorkOrder(actor, id);
  }

  transitionWorkOrder(actor, workOrderId, nextStatus) {
    this.authorize(actor, ['manager', 'dispatcher', 'technician']);
    const current = this.getWorkOrder(actor, workOrderId);
    const transitions = {
      new: ['scheduled', 'cancelled'],
      scheduled: ['in_progress', 'cancelled'],
      in_progress: ['completed', 'blocked'],
      blocked: ['in_progress', 'cancelled'],
      completed: [],
      cancelled: [],
    };
    if (!(transitions[current.status] || []).includes(nextStatus)) throw new ValidationError(`Invalid transition ${current.status} -> ${nextStatus}`);
    this.db.prepare('UPDATE work_order SET status = ?, version = version + 1, updated_at = ? WHERE tenant_id = ? AND id = ?')
      .run(nextStatus, nowIso(), actor.tenantId, workOrderId);
    this.audit(actor, 'work_order.transitioned', 'work_order', workOrderId, { from: current.status, to: nextStatus });
    return this.getWorkOrder(actor, workOrderId);
  }

  addAttachment(actor, workOrderId, { name, content }) {
    this.authorize(actor, ['manager', 'dispatcher', 'technician']);
    this.getWorkOrder(actor, workOrderId);
    const safeName = String(name || 'attachment.txt').replace(/[^a-zA-Z0-9._-]+/g, '-').slice(0, 80);
    const id = crypto.randomUUID();
    const tenantDir = path.join(this.storageRoot, actor.tenantId);
    fs.mkdirSync(tenantDir, { recursive: true });
    const relativePath = path.join(actor.tenantId, `${id}-${safeName}`);
    fs.writeFileSync(path.join(this.storageRoot, relativePath), String(content || ''), { encoding: 'utf8', flag: 'wx' });
    this.db.prepare('INSERT INTO attachment(id, tenant_id, work_order_id, name, relative_path, created_at) VALUES (?, ?, ?, ?, ?, ?)')
      .run(id, actor.tenantId, workOrderId, safeName, relativePath, nowIso());
    this.audit(actor, 'attachment.created', 'attachment', id, { workOrderId, name: safeName });
    return { id, name: safeName, workOrderId };
  }

  readAttachment(actor, attachmentId) {
    this.authorize(actor);
    const row = this.db.prepare('SELECT id, name, relative_path, work_order_id FROM attachment WHERE tenant_id = ? AND id = ?').get(actor.tenantId, attachmentId);
    if (!row) throw new ForbiddenError('Attachment not available in active organization');
    const absolute = path.resolve(this.storageRoot, row.relative_path);
    const tenantRoot = path.resolve(this.storageRoot, actor.tenantId) + path.sep;
    if (!absolute.startsWith(tenantRoot)) throw new ForbiddenError('Storage path escaped tenant namespace');
    return { ...row, content: fs.readFileSync(absolute, 'utf8') };
  }

  search(actor, query) {
    this.authorize(actor);
    const q = `%${String(query || '').trim()}%`;
    const customers = this.db.prepare('SELECT id, name, email FROM customer WHERE tenant_id = ? AND (name LIKE ? OR email LIKE ?) ORDER BY name LIMIT 20').all(actor.tenantId, q, q);
    const workOrders = this.db.prepare('SELECT id, title, status FROM work_order WHERE tenant_id = ? AND title LIKE ? ORDER BY updated_at DESC LIMIT 20').all(actor.tenantId, q);
    return { customers, workOrders };
  }

  enqueueNotification(actor, userId, message, idempotencyKey) {
    this.authorize(actor, ['manager', 'dispatcher']);
    const member = this.db.prepare('SELECT 1 AS ok FROM membership WHERE tenant_id = ? AND user_id = ?').get(actor.tenantId, userId);
    if (!member) throw new ForbiddenError('Notification recipient is outside active organization');
    const id = crypto.randomUUID();
    const at = nowIso();
    this.db.prepare(`
      INSERT OR IGNORE INTO job(id, tenant_id, kind, payload_json, status, attempts, next_run_at, idempotency_key, created_at, updated_at)
      VALUES (?, ?, 'notify', ?, 'queued', 0, ?, ?, ?, ?)
    `).run(id, actor.tenantId, JSON.stringify({ userId, message }), at, idempotencyKey, at, at);
    return this.db.prepare('SELECT * FROM job WHERE idempotency_key = ?').get(idempotencyKey);
  }

  processNextJob({ failProvider = false } = {}) {
    const job = this.db.prepare("SELECT * FROM job WHERE status IN ('queued','retry') AND next_run_at <= ? ORDER BY created_at LIMIT 1").get(nowIso());
    if (!job) return null;
    const payload = JSON.parse(job.payload_json);
    if (failProvider) {
      this.db.prepare("UPDATE job SET status = 'retry', attempts = attempts + 1, last_error = 'provider_unavailable', next_run_at = ?, updated_at = ? WHERE id = ?")
        .run(nowIso(), nowIso(), job.id);
      return { id: job.id, status: 'retry', tenantId: job.tenant_id, error: 'provider_unavailable' };
    }
    if (job.kind === 'notify') {
      const member = this.db.prepare('SELECT 1 AS ok FROM membership WHERE tenant_id = ? AND user_id = ?').get(job.tenant_id, payload.userId);
      if (!member) {
        this.db.prepare("UPDATE job SET status = 'failed', attempts = attempts + 1, last_error = 'recipient_not_in_tenant', updated_at = ? WHERE id = ?").run(nowIso(), job.id);
        return { id: job.id, status: 'failed', tenantId: job.tenant_id };
      }
      this.db.prepare('INSERT INTO notification(id, tenant_id, user_id, message, created_at, read_at) VALUES (?, ?, ?, ?, ?, NULL)')
        .run(crypto.randomUUID(), job.tenant_id, payload.userId, payload.message, nowIso());
    }
    this.db.prepare("UPDATE job SET status = 'done', attempts = attempts + 1, last_error = NULL, updated_at = ? WHERE id = ?").run(nowIso(), job.id);
    return { id: job.id, status: 'done', tenantId: job.tenant_id };
  }

  notifications(actor) {
    this.authorize(actor);
    return this.db.prepare('SELECT id, message, created_at, read_at FROM notification WHERE tenant_id = ? AND user_id = ? ORDER BY created_at DESC').all(actor.tenantId, actor.userId);
  }

  recordBillingEvent(tenantId, event) {
    const organization = this.db.prepare('SELECT id FROM organization WHERE id = ?').get(tenantId);
    if (!organization) throw new ValidationError('Unknown tenant');
    const providerEventId = String(event.providerEventId || '').trim();
    const providerVersion = Number(event.providerVersion);
    const eventType = String(event.type || '').trim();
    if (!providerEventId || !Number.isInteger(providerVersion) || providerVersion < 1) throw new ValidationError('Provider event id/version required');
    const existing = this.db.prepare('SELECT * FROM billing_event WHERE provider_event_id = ?').get(providerEventId);
    if (existing) return { duplicate: true, applied: Boolean(existing.applied), entitlement: this.entitlement(tenantId) };
    const current = this.entitlement(tenantId);
    const map = {
      'subscription.active': 'active',
      'subscription.past_due': 'restricted',
      'subscription.cancelled': 'inactive',
    };
    if (!map[eventType]) throw new ValidationError('Unsupported billing event');
    const applied = providerVersion >= Number(current.provider_version);
    this.db.prepare('INSERT INTO billing_event(id, tenant_id, provider_event_id, provider_version, event_type, payload_json, applied, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
      .run(crypto.randomUUID(), tenantId, providerEventId, providerVersion, eventType, JSON.stringify(event), applied ? 1 : 0, nowIso());
    if (applied) {
      this.db.prepare('UPDATE entitlement SET status = ?, provider_version = ?, updated_at = ? WHERE tenant_id = ?')
        .run(map[eventType], providerVersion, nowIso(), tenantId);
      this.permissionCache.clear();
    }
    return { duplicate: false, applied, entitlement: this.entitlement(tenantId) };
  }

  entitlement(tenantId) {
    return this.db.prepare('SELECT tenant_id, plan, status, provider_version, updated_at FROM entitlement WHERE tenant_id = ?').get(tenantId);
  }

  supportView(actor, targetTenant) {
    if (!actor || actor.platformRole !== 'support') throw new ForbiddenError('Platform support role required');
    if (!targetTenant) throw new ValidationError('Explicit tenant context is required');
    const organization = this.db.prepare('SELECT id, name FROM organization WHERE id = ?').get(targetTenant);
    if (!organization) throw new ValidationError('Unknown tenant context');
    this.db.prepare('INSERT INTO audit_log(id, tenant_id, actor_user_id, action, target_type, target_id, detail_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
      .run(crypto.randomUUID(), targetTenant, actor.userId, 'support.tenant_viewed', 'organization', targetTenant, JSON.stringify({ explicitTenantContext: true }), nowIso());
    return {
      organization,
      customers: this.db.prepare('SELECT id, name, email FROM customer WHERE tenant_id = ? ORDER BY name').all(targetTenant),
      workOrders: this.db.prepare('SELECT id, title, status FROM work_order WHERE tenant_id = ? ORDER BY updated_at DESC').all(targetTenant),
    };
  }

  audit(actor, action, targetType, targetId, detail = {}) {
    this.db.prepare('INSERT INTO audit_log(id, tenant_id, actor_user_id, action, target_type, target_id, detail_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)')
      .run(crypto.randomUUID(), actor.tenantId, actor.userId, action, targetType, targetId || null, JSON.stringify(detail), nowIso());
  }

  auditForTenant(actor, tenantId) {
    if (actor.platformRole === 'support') {
      if (!tenantId) throw new ValidationError('Explicit tenant context is required');
    } else {
      this.authorize(actor, ['manager']);
      if (actor.tenantId !== tenantId) throw new ForbiddenError();
    }
    return this.db.prepare('SELECT action, target_type, target_id, actor_user_id, detail_json, created_at FROM audit_log WHERE tenant_id = ? ORDER BY created_at DESC LIMIT 100').all(tenantId);
  }

  importCustomers(actor, csvText, batchKey) {
    this.authorize(actor, ['manager', 'dispatcher']);
    const lines = String(csvText || '').trim().split(/\r?\n/).filter(Boolean);
    if (!lines.length) throw new ValidationError('CSV content required');
    const header = lines.shift().split(',').map((value) => value.trim().toLowerCase());
    if (header[0] !== 'name' || header[1] !== 'email') throw new ValidationError('CSV header must begin name,email');
    const results = [];
    lines.forEach((line, index) => {
      const rowNumber = index + 2;
      const [nameRaw = '', emailRaw = '', phoneRaw = ''] = line.split(',').map((value) => value.trim());
      const rowKey = crypto.createHash('sha256').update(`${nameRaw}|${emailRaw}|${phoneRaw}`).digest('hex');
      const prior = this.db.prepare('SELECT status, error, customer_id FROM import_row WHERE tenant_id = ? AND batch_key = ? AND row_number = ?').get(actor.tenantId, batchKey, rowNumber);
      if (prior?.status === 'imported') {
        results.push({ rowNumber, status: 'imported', customerId: prior.customer_id, replay: true });
        return;
      }
      let status = 'failed';
      let error = null;
      let customerId = null;
      if (!nameRaw || !emailRaw.includes('@')) {
        error = 'invalid_name_or_email';
      } else {
        const existing = this.db.prepare('SELECT id FROM customer WHERE tenant_id = ? AND email = ?').get(actor.tenantId, emailRaw.toLowerCase());
        if (existing) {
          customerId = existing.id;
          status = 'imported';
        } else {
          customerId = crypto.randomUUID();
          this.db.prepare('INSERT INTO customer(id, tenant_id, name, email, phone, created_at) VALUES (?, ?, ?, ?, ?, ?)')
            .run(customerId, actor.tenantId, nameRaw, emailRaw.toLowerCase(), phoneRaw || null, nowIso());
          status = 'imported';
        }
      }
      this.db.prepare(`
        INSERT INTO import_row(tenant_id, batch_key, row_number, row_key, status, error, customer_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(tenant_id, batch_key, row_number)
        DO UPDATE SET row_key = excluded.row_key, status = excluded.status, error = excluded.error, customer_id = excluded.customer_id
      `).run(actor.tenantId, batchKey, rowNumber, rowKey, status, error, customerId);
      results.push({ rowNumber, status, error, customerId, replay: false });
    });
    this.audit(actor, 'customer.imported', 'import_batch', batchKey, { imported: results.filter((r) => r.status === 'imported').length, failed: results.filter((r) => r.status === 'failed').length });
    return results;
  }

  exportCustomers(actor) {
    this.authorize(actor, ['manager', 'dispatcher', 'billing']);
    const rows = this.db.prepare('SELECT name, email, COALESCE(phone, "") AS phone FROM customer WHERE tenant_id = ? ORDER BY name').all(actor.tenantId);
    const escape = (value) => `"${String(value).replaceAll('"', '""')}"`;
    return ['name,email,phone', ...rows.map((row) => [row.name, row.email, row.phone].map(escape).join(','))].join('\n') + '\n';
  }
}

module.exports = {
  RelayStore,
  ForbiddenError,
  ValidationError,
};
