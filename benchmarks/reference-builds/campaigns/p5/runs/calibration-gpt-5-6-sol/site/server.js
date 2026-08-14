const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { RelayStore, ForbiddenError, ValidationError } = require('./src/store');
const { parseCookies } = require('./src/auth');
const {
  loginPage,
  dashboardPage,
  customersPage,
  workOrdersPage,
  billingPage,
  importExportPage,
  adminPage,
  notFoundPage,
} = require('./src/render');

const ROOT = __dirname;

function securityHeaders(contentType = 'text/html; charset=utf-8') {
  return {
    'content-type': contentType,
    'content-security-policy': "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'",
    'referrer-policy': 'no-referrer',
    'x-content-type-options': 'nosniff',
    'x-frame-options': 'DENY',
    'permissions-policy': 'camera=(), microphone=(), geolocation=()',
    'cache-control': 'no-store',
  };
}

function send(res, status, body, headers = {}) {
  const payload = Buffer.isBuffer(body) ? body : Buffer.from(String(body));
  res.writeHead(status, { ...securityHeaders(headers['content-type']), 'content-length': payload.length, ...headers });
  res.end(payload);
}

function json(res, status, body, headers = {}) {
  send(res, status, JSON.stringify(body), { 'content-type': 'application/json; charset=utf-8', ...headers });
}

function redirect(res, location, status = 303) {
  res.writeHead(status, { ...securityHeaders('text/plain; charset=utf-8'), location, 'content-length': 0 });
  res.end();
}

async function readBody(req, limit = 1_000_000) {
  let size = 0;
  const chunks = [];
  for await (const chunk of req) {
    size += chunk.length;
    if (size > limit) throw new ValidationError('Request body too large');
    chunks.push(chunk);
  }
  const raw = Buffer.concat(chunks).toString('utf8');
  if (!raw) return {};
  const type = String(req.headers['content-type'] || '').split(';')[0];
  if (type === 'application/json') {
    try { return JSON.parse(raw); } catch { throw new ValidationError('Malformed JSON'); }
  }
  if (type === 'application/x-www-form-urlencoded') return Object.fromEntries(new URLSearchParams(raw));
  return { raw };
}

function sameOrigin(req) {
  const origin = req.headers.origin;
  if (!origin) return true;
  const expected = process.env.RELAYOPS_ORIGIN || `http://${req.headers.host}`;
  return origin === expected;
}

function sessionCookie(token) {
  const secure = String(process.env.RELAYOPS_ORIGIN || '').startsWith('https://');
  return `relayops_session=${encodeURIComponent(token)}; HttpOnly; SameSite=Lax; Path=/; Max-Age=43200${secure ? '; Secure' : ''}`;
}

function clearSessionCookie() {
  return 'relayops_session=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0';
}

function actorFor(req, store) {
  const token = parseCookies(req.headers.cookie || '').relayops_session;
  return store.actorFromToken(token);
}

function requireActor(req, store) {
  const actor = actorFor(req, store);
  if (!actor) throw new ForbiddenError('Authentication required');
  return actor;
}

function serveAsset(res, pathname) {
  const assets = {
    '/assets/styles.css': ['public/styles.css', 'text/css; charset=utf-8'],
    '/assets/app.js': ['public/app.js', 'application/javascript; charset=utf-8'],
  };
  const item = assets[pathname];
  if (!item) return false;
  const content = fs.readFileSync(path.join(ROOT, item[0]));
  send(res, 200, content, { 'content-type': item[1], 'cache-control': 'public, max-age=300' });
  return true;
}

function createApp({ store = new RelayStore() } = {}) {
  const server = http.createServer(async (req, res) => {
    const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
    const pathname = url.pathname;
    try {
      if (serveAsset(res, pathname)) return;

      if (pathname === '/api/health' && req.method === 'GET') {
        return json(res, 200, { ok: true, service: 'relayops', campaign: 'p5-calibration' });
      }

      if (pathname === '/api/login' && req.method === 'POST') {
        if (!sameOrigin(req)) throw new ForbiddenError('Cross-origin mutation rejected');
        const body = await readBody(req);
        const login = store.login(body.email, body.password, body.tenantId || null);
        if (!login) return json(res, 401, { error: 'Invalid credentials or organization membership' });
        return json(res, 200, { actor: login.actor }, { 'set-cookie': sessionCookie(login.token) });
      }

      if (pathname === '/api/logout' && req.method === 'POST') {
        const cookies = parseCookies(req.headers.cookie || '');
        if (cookies.relayops_session) store.logout(cookies.relayops_session);
        return json(res, 200, { ok: true }, { 'set-cookie': clearSessionCookie() });
      }

      if (pathname === '/login' && req.method === 'GET') {
        const actor = actorFor(req, store);
        if (actor) return redirect(res, actor.platformRole ? '/admin' : '/dashboard');
        return send(res, 200, loginPage());
      }

      if (pathname === '/' && req.method === 'GET') {
        const actor = actorFor(req, store);
        return redirect(res, actor ? (actor.platformRole ? '/admin' : '/dashboard') : '/login');
      }

      if (pathname === '/api/me' && req.method === 'GET') {
        const actor = requireActor(req, store);
        return json(res, 200, { actor });
      }

      if (pathname === '/dashboard' && req.method === 'GET') {
        const actor = actorFor(req, store);
        if (!actor) return redirect(res, '/login');
        if (actor.platformRole) return redirect(res, '/admin');
        const organization = store.organization(actor);
        return send(res, 200, dashboardPage(actor, organization, store.listWorkOrders(actor), store.notifications(actor), store.entitlement(actor.tenantId)));
      }

      if (pathname === '/customers' && req.method === 'GET') {
        const actor = actorFor(req, store);
        if (!actor) return redirect(res, '/login');
        if (actor.platformRole) return redirect(res, '/admin');
        const query = url.searchParams.get('q') || '';
        return send(res, 200, customersPage(actor, store.listCustomers(actor, query), query));
      }

      if (pathname === '/work-orders' && req.method === 'GET') {
        const actor = actorFor(req, store);
        if (!actor) return redirect(res, '/login');
        if (actor.platformRole) return redirect(res, '/admin');
        const filters = { status: url.searchParams.get('status') || '', query: url.searchParams.get('q') || '' };
        return send(res, 200, workOrdersPage(actor, store.listWorkOrders(actor, filters), store.listCustomers(actor), filters));
      }

      if (pathname === '/billing' && req.method === 'GET') {
        const actor = actorFor(req, store);
        if (!actor) return redirect(res, '/login');
        if (actor.platformRole) return redirect(res, '/admin');
        store.authorize(actor);
        return send(res, 200, billingPage(actor, store.entitlement(actor.tenantId)));
      }

      if (pathname === '/import-export' && req.method === 'GET') {
        const actor = actorFor(req, store);
        if (!actor) return redirect(res, '/login');
        if (actor.platformRole) return redirect(res, '/admin');
        store.authorize(actor, ['manager', 'dispatcher', 'billing']);
        return send(res, 200, importExportPage(actor));
      }

      if (pathname === '/admin' && req.method === 'GET') {
        const actor = actorFor(req, store);
        if (!actor) return redirect(res, '/login');
        if (actor.platformRole !== 'support') throw new ForbiddenError('Platform support role required');
        const tenant = url.searchParams.get('tenant') || '';
        const view = tenant ? store.supportView(actor, tenant) : null;
        const auditRows = tenant ? store.auditForTenant(actor, tenant) : [];
        return send(res, 200, adminPage(actor, tenant, view, auditRows));
      }

      if (pathname === '/api/customers' && req.method === 'GET') {
        const actor = requireActor(req, store);
        return json(res, 200, { customers: store.listCustomers(actor, url.searchParams.get('q') || '') });
      }

      if (pathname === '/api/customers' && req.method === 'POST') {
        if (!sameOrigin(req)) throw new ForbiddenError('Cross-origin mutation rejected');
        const actor = requireActor(req, store);
        return json(res, 201, { customer: store.createCustomer(actor, await readBody(req)) });
      }

      if (pathname === '/api/work-orders' && req.method === 'GET') {
        const actor = requireActor(req, store);
        return json(res, 200, { workOrders: store.listWorkOrders(actor, { status: url.searchParams.get('status') || '', query: url.searchParams.get('q') || '' }) });
      }

      if (pathname === '/api/work-orders' && req.method === 'POST') {
        if (!sameOrigin(req)) throw new ForbiddenError('Cross-origin mutation rejected');
        const actor = requireActor(req, store);
        return json(res, 201, { workOrder: store.createWorkOrder(actor, await readBody(req)) });
      }

      const statusMatch = pathname.match(/^\/api\/work-orders\/([^/]+)\/status$/);
      if (statusMatch && req.method === 'POST') {
        if (!sameOrigin(req)) throw new ForbiddenError('Cross-origin mutation rejected');
        const actor = requireActor(req, store);
        const body = await readBody(req);
        return json(res, 200, { workOrder: store.transitionWorkOrder(actor, decodeURIComponent(statusMatch[1]), body.status) });
      }

      const attachmentCreate = pathname.match(/^\/api\/work-orders\/([^/]+)\/attachments$/);
      if (attachmentCreate && req.method === 'POST') {
        if (!sameOrigin(req)) throw new ForbiddenError('Cross-origin mutation rejected');
        const actor = requireActor(req, store);
        return json(res, 201, { attachment: store.addAttachment(actor, decodeURIComponent(attachmentCreate[1]), await readBody(req)) });
      }

      const attachmentRead = pathname.match(/^\/api\/attachments\/([^/]+)$/);
      if (attachmentRead && req.method === 'GET') {
        const actor = requireActor(req, store);
        return json(res, 200, { attachment: store.readAttachment(actor, decodeURIComponent(attachmentRead[1])) });
      }

      if (pathname === '/api/search' && req.method === 'GET') {
        const actor = requireActor(req, store);
        return json(res, 200, store.search(actor, url.searchParams.get('q') || ''));
      }

      if (pathname === '/api/notifications' && req.method === 'GET') {
        const actor = requireActor(req, store);
        return json(res, 200, { notifications: store.notifications(actor) });
      }

      if (pathname === '/api/notifications' && req.method === 'POST') {
        if (!sameOrigin(req)) throw new ForbiddenError('Cross-origin mutation rejected');
        const actor = requireActor(req, store);
        const body = await readBody(req);
        const key = String(body.idempotencyKey || crypto.randomUUID());
        return json(res, 202, { job: store.enqueueNotification(actor, body.userId, body.message, key) });
      }

      if (pathname === '/api/billing' && req.method === 'GET') {
        const actor = requireActor(req, store);
        store.authorize(actor);
        return json(res, 200, { entitlement: store.entitlement(actor.tenantId) });
      }

      if (pathname === '/api/billing/checkout' && req.method === 'POST') {
        if (!sameOrigin(req)) throw new ForbiddenError('Cross-origin mutation rejected');
        const actor = requireActor(req, store);
        store.authorize(actor, ['manager', 'billing']);
        const reference = `checkout_${crypto.randomBytes(8).toString('hex')}`;
        store.audit(actor, 'billing.checkout_intent_created', 'billing_checkout', reference, { entitlementChanged: false });
        return json(res, 201, { reference, entitlement: store.entitlement(actor.tenantId), note: 'Provider intent only; entitlement changes after reconciliation.' });
      }

      if (pathname === '/api/import' && req.method === 'POST') {
        if (!sameOrigin(req)) throw new ForbiddenError('Cross-origin mutation rejected');
        const actor = requireActor(req, store);
        const body = await readBody(req);
        return json(res, 200, { rows: store.importCustomers(actor, body.csv, String(body.batchKey || 'default')) });
      }

      if (pathname === '/api/export' && req.method === 'GET') {
        const actor = requireActor(req, store);
        const csv = store.exportCustomers(actor);
        return send(res, 200, csv, { 'content-type': 'text/csv; charset=utf-8', 'content-disposition': 'attachment; filename="relayops-customers.csv"' });
      }

      if (pathname === '/api/admin' && req.method === 'GET') {
        const actor = requireActor(req, store);
        const tenant = url.searchParams.get('tenant') || '';
        return json(res, 200, { view: store.supportView(actor, tenant), audit: store.auditForTenant(actor, tenant) });
      }

      if (pathname === '/api/test/billing-event' && req.method === 'POST') {
        if (process.env.RELAYOPS_ENABLE_TEST_FAILURES !== '1') return json(res, 404, { error: 'Not found' });
        if (req.headers['x-relayops-test-secret'] !== process.env.RELAYOPS_TEST_SECRET) throw new ForbiddenError('Test control secret required');
        const body = await readBody(req);
        return json(res, 200, store.recordBillingEvent(body.tenantId, body.event));
      }

      if (pathname === '/api/test/process-job' && req.method === 'POST') {
        if (process.env.RELAYOPS_ENABLE_TEST_FAILURES !== '1') return json(res, 404, { error: 'Not found' });
        if (req.headers['x-relayops-test-secret'] !== process.env.RELAYOPS_TEST_SECRET) throw new ForbiddenError('Test control secret required');
        const body = await readBody(req);
        return json(res, 200, { job: store.processNextJob({ failProvider: Boolean(body.failProvider) }) });
      }

      return send(res, 404, notFoundPage());
    } catch (error) {
      const status = error.statusCode || (error instanceof ForbiddenError ? 403 : error instanceof ValidationError ? 400 : 500);
      if (status >= 500) console.error(error);
      if (pathname.startsWith('/api/')) return json(res, status, { error: status >= 500 ? 'Internal server error' : error.message });
      if (status === 403 && !actorFor(req, store)) return redirect(res, '/login');
      return send(res, status, `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Error · RelayOps</title><link rel="stylesheet" href="/assets/styles.css"></head><body><main class="not-found"><p class="eyebrow">${status}</p><h1>${status === 403 ? 'Access denied.' : 'Something went wrong.'}</h1><p>${status >= 500 ? 'The request could not be completed.' : String(error.message).replaceAll('<','&lt;')}</p><a class="button primary" href="/">Return to workspace</a></main></body></html>`);
    }
  });
  return { server, store };
}

if (require.main === module) {
  const port = Number(process.env.PORT || 4173);
  const { server } = createApp();
  server.listen(port, '0.0.0.0', () => {
    console.log(`RelayOps calibration listening on http://0.0.0.0:${port}`);
  });
}

module.exports = { createApp };
