const test = require('node:test');
const assert = require('node:assert/strict');
const { createApp } = require('../server');
const { fixtureStore, writeEvidence } = require('./helpers');

async function startFixture() {
  const fx = fixtureStore();
  const { server } = createApp({ store: fx.store });
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const port = server.address().port;
  const base = `http://127.0.0.1:${port}`;
  return {
    ...fx,
    server,
    base,
    async stop() {
      await new Promise((resolve) => server.close(resolve));
      fx.cleanup();
    },
  };
}

async function login(base, email, password) {
  const response = await fetch(`${base}/api/login`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', origin: base },
    body: JSON.stringify({ email, password }),
    redirect: 'manual',
  });
  const cookie = response.headers.get('set-cookie')?.split(';')[0];
  return { response, cookie, body: await response.json() };
}

async function request(base, pathname, cookie, options = {}) {
  return fetch(`${base}${pathname}`, {
    redirect: 'manual',
    ...options,
    headers: {
      ...(cookie ? { cookie } : {}),
      ...(options.body ? { 'content-type': 'application/json', origin: base } : {}),
      ...(options.headers || {}),
    },
  });
}

test('HTTP auth lifecycle enters a protected organization workspace', async () => {
  const fx = await startFixture();
  try {
    const anonymous = await request(fx.base, '/dashboard', null);
    assert.equal(anonymous.status, 303);
    assert.equal(anonymous.headers.get('location'), '/login');

    const invalid = await login(fx.base, 'manager@northline.test', 'wrong');
    assert.equal(invalid.response.status, 401);

    const signed = await login(fx.base, 'manager@northline.test', 'relayops-demo');
    assert.equal(signed.response.status, 200);
    assert.ok(signed.cookie?.startsWith('relayops_session='));
    assert.equal(signed.body.actor.tenantId, 'northline');

    const dashboard = await request(fx.base, '/dashboard', signed.cookie);
    assert.equal(dashboard.status, 200);
    const html = await dashboard.text();
    assert.match(html, /Operations overview/);
    assert.match(html, /Northline Facilities/);
    assert.doesNotMatch(html, /Harbor Service Group/);

    const logout = await request(fx.base, '/api/logout', signed.cookie, { method: 'POST', body: '{}' });
    assert.equal(logout.status, 200);
    const after = await request(fx.base, '/api/me', signed.cookie);
    assert.equal(after.status, 403);

    writeEvidence('http-auth-flow', {
      anonymous_protected_redirect: true,
      invalid_credentials_status: invalid.response.status,
      authenticated_tenant: signed.body.actor.tenantId,
      protected_dashboard_status: dashboard.status,
      foreign_tenant_name_exposed: false,
      logout_invalidated_session: after.status === 403,
    });
  } finally { await fx.stop(); }
});

test('HTTP operational flow persists customer and work order then filters search', async () => {
  const fx = await startFixture();
  try {
    const signed = await login(fx.base, 'manager@northline.test', 'relayops-demo');
    const createCustomer = await request(fx.base, '/api/customers', signed.cookie, {
      method: 'POST',
      body: JSON.stringify({ name: 'Cedar Medical', email: 'ops@cedarmedical.test', phone: '+1 415 555 0177' }),
    });
    assert.equal(createCustomer.status, 201);
    const customer = (await createCustomer.json()).customer;

    const createOrder = await request(fx.base, '/api/work-orders', signed.cookie, {
      method: 'POST',
      body: JSON.stringify({ customerId: customer.id, title: 'Calibrate rooftop controls', priority: 'high' }),
    });
    assert.equal(createOrder.status, 201);
    const workOrder = (await createOrder.json()).workOrder;
    assert.equal(workOrder.status, 'new');

    const transition = await request(fx.base, `/api/work-orders/${workOrder.id}/status`, signed.cookie, {
      method: 'POST',
      body: JSON.stringify({ status: 'scheduled' }),
    });
    assert.equal(transition.status, 200);
    assert.equal((await transition.json()).workOrder.status, 'scheduled');

    const search = await request(fx.base, '/api/search?q=Cedar', signed.cookie);
    const searchBody = await search.json();
    assert.equal(searchBody.customers[0].id, customer.id);
    assert.equal(searchBody.workOrders[0].id, workOrder.id);

    const foreign = await request(fx.base, '/api/attachments/nonexistent-harbor-object', signed.cookie);
    assert.equal(foreign.status, 403);

    writeEvidence('http-operational-flow', {
      customer_created_status: createCustomer.status,
      work_order_created_status: createOrder.status,
      work_order_transition: 'new -> scheduled',
      search_found_tenant_customer: true,
      search_found_tenant_work_order: true,
      unknown_or_foreign_object_status: foreign.status,
    });
  } finally { await fx.stop(); }
});

test('HTTP support path requires explicit tenant context and records audit', async () => {
  const fx = await startFixture();
  try {
    const manager = await login(fx.base, 'manager@northline.test', 'relayops-demo');
    const managerAdmin = await request(fx.base, '/api/admin?tenant=northline', manager.cookie);
    assert.equal(managerAdmin.status, 403);

    const support = await login(fx.base, 'support@relayops.test', 'relayops-support');
    const missingContext = await request(fx.base, '/api/admin', support.cookie);
    assert.equal(missingContext.status, 400);
    const explicit = await request(fx.base, '/api/admin?tenant=harbor', support.cookie);
    assert.equal(explicit.status, 200);
    const payload = await explicit.json();
    assert.equal(payload.view.organization.id, 'harbor');
    assert.equal(payload.view.customers.some((row) => row.id === 'c-north-1'), false);
    assert.equal(payload.audit[0].action, 'support.tenant_viewed');

    writeEvidence('http-admin-flow', {
      manager_privileged_attempt_status: managerAdmin.status,
      support_missing_context_status: missingContext.status,
      support_explicit_context_status: explicit.status,
      target_tenant: payload.view.organization.id,
      foreign_customer_exposed: false,
      audit_action: payload.audit[0].action,
    });
  } finally { await fx.stop(); }
});

test('security headers and 404 behavior are explicit', async () => {
  const fx = await startFixture();
  try {
    const loginPage = await request(fx.base, '/login', null);
    assert.equal(loginPage.status, 200);
    assert.match(loginPage.headers.get('content-security-policy'), /default-src 'self'/);
    assert.equal(loginPage.headers.get('x-frame-options'), 'DENY');
    const missing = await request(fx.base, '/does-not-exist', null);
    assert.equal(missing.status, 404);
    const html = await missing.text();
    assert.match(html, /noindex,nofollow/);
    assert.doesNotMatch(html, /rel="canonical"/);
    writeEvidence('http-security', {
      csp: loginPage.headers.get('content-security-policy'),
      x_frame_options: loginPage.headers.get('x-frame-options'),
      not_found_status: missing.status,
      not_found_noindex: true,
      not_found_has_canonical: false,
    });
  } finally { await fx.stop(); }
});
