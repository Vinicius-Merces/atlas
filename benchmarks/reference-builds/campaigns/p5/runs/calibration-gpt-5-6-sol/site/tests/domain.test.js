const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { ForbiddenError, ValidationError } = require('../src/store');
const { fixtureStore, actor, writeEvidence } = require('./helpers');

function denied(fn) {
  assert.throws(fn, (error) => error instanceof ForbiddenError && error.statusCode === 403);
}

test('authentication binds normal sessions to organization membership and rejects invalid credentials', () => {
  const fx = fixtureStore();
  try {
    assert.equal(fx.store.login('manager@northline.test', 'wrong-password'), null);
    const north = fx.store.login('manager@northline.test', 'relayops-demo');
    const harbor = fx.store.login('manager@harbor.test', 'relayops-demo');
    const support = fx.store.login('support@relayops.test', 'relayops-support');
    assert.equal(north.actor.tenantId, 'northline');
    assert.equal(north.actor.role, 'manager');
    assert.equal(harbor.actor.tenantId, 'harbor');
    assert.equal(support.actor.tenantId, null);
    assert.equal(support.actor.platformRole, 'support');
    assert.equal(fx.store.actorFromToken(north.token).tenantId, 'northline');
    fx.store.logout(north.token);
    assert.equal(fx.store.actorFromToken(north.token), null);
    writeEvidence('auth-membership', {
      checks: {
        invalid_password_denied: true,
        northline_session_tenant: north.actor.tenantId,
        harbor_session_tenant: harbor.actor.tenantId,
        support_has_no_implicit_tenant: support.actor.tenantId === null,
        logout_invalidates_session: true,
      },
    });
  } finally { fx.cleanup(); }
});

test('cross-tenant database object reads and writes are denied', () => {
  const fx = fixtureStore();
  try {
    const north = actor(fx.store, 'manager@northline.test');
    const harbor = actor(fx.store, 'manager@harbor.test');
    denied(() => fx.store.getCustomer(north, 'c-harbor-1'));
    denied(() => fx.store.getCustomer(harbor, 'c-north-1'));
    denied(() => fx.store.getWorkOrder(north, 'wo-harbor-1'));
    denied(() => fx.store.createWorkOrder(harbor, { customerId: 'c-north-1', title: 'Cross tenant attempt', priority: 'normal' }));
    assert.equal(fx.store.listCustomers(north).some((row) => row.id === 'c-harbor-1'), false);
    assert.equal(fx.store.listWorkOrders(harbor).some((row) => row.id === 'wo-north-1'), false);
    writeEvidence('tenant-database', {
      attempts: [
        { source_tenant: 'northline', target_tenant: 'harbor', operation: 'customer-read', outcome: 'denied' },
        { source_tenant: 'harbor', target_tenant: 'northline', operation: 'customer-read', outcome: 'denied' },
        { source_tenant: 'northline', target_tenant: 'harbor', operation: 'work-order-read', outcome: 'denied' },
        { source_tenant: 'harbor', target_tenant: 'northline', operation: 'work-order-create-with-foreign-customer', outcome: 'denied' },
      ],
      tenant_filtered_lists: true,
    });
  } finally { fx.cleanup(); }
});

test('tenant storage namespace denies cross-tenant reads and foreign work-order writes', () => {
  const fx = fixtureStore();
  try {
    const north = actor(fx.store, 'manager@northline.test');
    const harbor = actor(fx.store, 'manager@harbor.test');
    const attachment = fx.store.addAttachment(north, 'wo-north-1', { name: 'compressor-note.txt', content: 'Northline private service note' });
    assert.equal(fx.store.readAttachment(north, attachment.id).content, 'Northline private service note');
    denied(() => fx.store.readAttachment(harbor, attachment.id));
    denied(() => fx.store.addAttachment(harbor, 'wo-north-1', { name: 'foreign.txt', content: 'should never write' }));
    writeEvidence('tenant-storage', {
      attempts: [
        { source_tenant: 'harbor', target_tenant: 'northline', operation: 'attachment-read', outcome: 'denied', attachment_id: attachment.id },
        { source_tenant: 'harbor', target_tenant: 'northline', operation: 'attachment-write', outcome: 'denied', work_order_id: 'wo-north-1' },
      ],
      authorized_read: true,
      namespace_root: 'tenant-scoped filesystem path plus tenant-filtered attachment row',
    });
  } finally { fx.cleanup(); }
});

test('search is tenant-filtered and cannot discover foreign records', () => {
  const fx = fixtureStore();
  try {
    const north = actor(fx.store, 'manager@northline.test');
    const harbor = actor(fx.store, 'manager@harbor.test');
    const northLeak = fx.store.search(north, 'Beacon');
    const harborLeak = fx.store.search(harbor, 'Atlas');
    assert.deepEqual(northLeak.customers, []);
    assert.deepEqual(northLeak.workOrders, []);
    assert.deepEqual(harborLeak.customers, []);
    assert.deepEqual(harborLeak.workOrders, []);
    assert.equal(fx.store.search(north, 'Atlas').customers[0].id, 'c-north-1');
    writeEvidence('tenant-search', {
      attempts: [
        { source_tenant: 'northline', target_tenant: 'harbor', operation: 'search-Beacon', outcome: 'denied', leaked_records: 0 },
        { source_tenant: 'harbor', target_tenant: 'northline', operation: 'search-Atlas', outcome: 'denied', leaked_records: 0 },
      ],
      positive_tenant_search: true,
    });
  } finally { fx.cleanup(); }
});

test('authorization cache cannot preserve a revoked membership and jobs keep tenant context', () => {
  const fx = fixtureStore();
  try {
    const manager = actor(fx.store, 'manager@northline.test');
    const snapshot = fx.store.permissionSnapshot(manager);
    assert.equal(snapshot.role, 'manager');
    fx.store.revokeMembership(manager.userId, 'northline');
    denied(() => fx.store.authorize(manager));

    const dispatcher = actor(fx.store, 'dispatch@northline.test');
    const first = fx.store.enqueueNotification(dispatcher, 'u-north-tech', 'Gate B compressor is ready', 'notify:gate-b');
    const duplicate = fx.store.enqueueNotification(dispatcher, 'u-north-tech', 'Gate B compressor is ready', 'notify:gate-b');
    assert.equal(first.id, duplicate.id);
    const failed = fx.store.processNextJob({ failProvider: true });
    assert.equal(failed.status, 'retry');
    assert.equal(failed.tenantId, 'northline');
    const recovered = fx.store.processNextJob({ failProvider: false });
    assert.equal(recovered.status, 'done');
    assert.equal(recovered.tenantId, 'northline');
    assert.equal(fx.store.processNextJob(), null);
    writeEvidence('tenant-cache-jobs', {
      cache: { stale_membership_after_revoke: 'denied', cache_invalidated: true },
      jobs: {
        idempotency_key_deduplicated: true,
        duplicate_job_id: first.id,
        tenant_context: recovered.tenantId,
        provider_failure_status: failed.status,
        retry_recovery_status: recovered.status,
        uncontrolled_duplicate_effects: 0,
      },
    });
  } finally { fx.cleanup(); }
});

test('notifications reject foreign recipients and recover after provider failure', () => {
  const fx = fixtureStore();
  try {
    const dispatcher = actor(fx.store, 'dispatch@northline.test');
    denied(() => fx.store.enqueueNotification(dispatcher, 'u-harbor-manager', 'Foreign notice', 'foreign-notice'));
    fx.store.enqueueNotification(dispatcher, 'u-north-tech', 'Technician dispatch changed', 'north-notice');
    assert.equal(fx.store.processNextJob({ failProvider: true }).status, 'retry');
    assert.equal(fx.store.processNextJob({ failProvider: false }).status, 'done');
    const tech = actor(fx.store, 'tech@northline.test');
    const notices = fx.store.notifications(tech);
    assert.equal(notices.length, 1);
    assert.match(notices[0].message, /dispatch changed/);
    writeEvidence('notifications', {
      foreign_recipient: { source_tenant: 'northline', target_tenant: 'harbor', outcome: 'denied' },
      provider_failure: 'retry',
      recovery: 'done',
      tenant_delivery_count: notices.length,
    });
  } finally { fx.cleanup(); }
});

test('billing events are idempotent, order-aware and reconcile application entitlements', () => {
  const fx = fixtureStore();
  try {
    const manager = actor(fx.store, 'manager@northline.test');
    assert.equal(fx.store.entitlement('northline').status, 'active');
    const cancel = fx.store.recordBillingEvent('northline', { providerEventId: 'evt-v3-cancel', providerVersion: 3, type: 'subscription.cancelled' });
    assert.equal(cancel.applied, true);
    assert.equal(cancel.entitlement.status, 'inactive');
    denied(() => fx.store.authorize(manager));

    const stale = fx.store.recordBillingEvent('northline', { providerEventId: 'evt-v2-active', providerVersion: 2, type: 'subscription.active' });
    assert.equal(stale.applied, false);
    assert.equal(stale.entitlement.status, 'inactive');

    const duplicate = fx.store.recordBillingEvent('northline', { providerEventId: 'evt-v3-cancel', providerVersion: 3, type: 'subscription.cancelled' });
    assert.equal(duplicate.duplicate, true);

    const restore = fx.store.recordBillingEvent('northline', { providerEventId: 'evt-v4-active', providerVersion: 4, type: 'subscription.active' });
    assert.equal(restore.applied, true);
    assert.equal(restore.entitlement.status, 'active');
    assert.equal(fx.store.authorize(manager).entitlementStatus, 'active');
    writeEvidence('billing-entitlements', {
      provider_is_not_direct_authority: true,
      cancellation: { version: 3, applied: true, resulting_entitlement: 'inactive', protected_action_after_revoke: 'denied' },
      out_of_order: { version: 2, applied: false, entitlement_remained: 'inactive' },
      duplicate: { provider_event_id: 'evt-v3-cancel', duplicate: true },
      reconciliation: { version: 4, applied: true, resulting_entitlement: 'active' },
    });
  } finally { fx.cleanup(); }
});

test('support requires platform privilege and explicit tenant context with audit evidence', () => {
  const fx = fixtureStore();
  try {
    const manager = actor(fx.store, 'manager@northline.test');
    denied(() => fx.store.supportView(manager, 'northline'));
    const support = actor(fx.store, 'support@relayops.test', 'relayops-support');
    assert.throws(() => fx.store.supportView(support, ''), ValidationError);
    const view = fx.store.supportView(support, 'northline');
    assert.equal(view.organization.id, 'northline');
    assert.equal(view.customers.some((row) => row.id === 'c-harbor-1'), false);
    const audit = fx.store.auditForTenant(support, 'northline');
    assert.equal(audit[0].action, 'support.tenant_viewed');
    const detail = JSON.parse(audit[0].detail_json);
    assert.equal(detail.explicitTenantContext, true);
    writeEvidence('admin-audit', {
      non_support_attempt: { outcome: 'denied' },
      missing_tenant_context: { outcome: 'denied' },
      privileged_action: 'support.tenant_viewed',
      target_tenant: 'northline',
      foreign_customer_visible: false,
      audit_recorded: true,
      explicit_tenant_context: true,
    });
  } finally { fx.cleanup(); }
});

test('CSV import exposes partial failure, safely replays successful rows, and export stays tenant-scoped', () => {
  const fx = fixtureStore();
  try {
    const manager = actor(fx.store, 'manager@northline.test');
    const csv = 'name,email,phone\nOrchid Hotel,facilities@orchid.test,+1 415 555 0188\nMissing Email,,+1 415 555 0199';
    const first = fx.store.importCustomers(manager, csv, 'batch-a');
    assert.equal(first[0].status, 'imported');
    assert.equal(first[1].status, 'failed');
    assert.equal(first[1].error, 'invalid_name_or_email');
    const second = fx.store.importCustomers(manager, csv, 'batch-a');
    assert.equal(second[0].status, 'imported');
    assert.equal(second[0].replay, true);
    const exportCsv = fx.store.exportCustomers(manager);
    assert.match(exportCsv, /Orchid Hotel/);
    assert.doesNotMatch(exportCsv, /Beacon Kitchens/);
    writeEvidence('import-export', {
      row_validation: true,
      first_run: first,
      safe_retry: { successful_row_replayed_without_duplicate: second[0].replay === true },
      export: { tenant: 'northline', contains_northline_import: true, contains_harbor_customer: false },
    });
  } finally { fx.cleanup(); }
});

test('browser-visible assets do not contain privileged/provider secret identifiers', () => {
  const browserVisible = [
    path.resolve(__dirname, '../public/app.js'),
    path.resolve(__dirname, '../public/styles.css'),
    path.resolve(__dirname, '../src/render.js'),
  ].map((file) => fs.readFileSync(file, 'utf8')).join('\n');
  const forbidden = ['RELAYOPS_TEST_SECRET', 'STRIPE_SECRET', 'SERVICE_ROLE_KEY', 'SUPABASE_SERVICE_ROLE', 'relayops-calibration-secret'];
  for (const token of forbidden) assert.equal(browserVisible.includes(token), false, `browser-visible source contains ${token}`);
  writeEvidence('secret-boundary', {
    scanned_surfaces: ['public/app.js', 'public/styles.css', 'src/render.js'],
    forbidden_identifiers: forbidden,
    exposed_privileged_secrets: 0,
    server_only_test_control: true,
  });
});
