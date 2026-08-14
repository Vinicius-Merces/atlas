function esc(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function statusBadge(status) {
  return `<span class="status status-${esc(status)}">${esc(String(status).replaceAll('_', ' '))}</span>`;
}

function nav(actor) {
  if (!actor) return '';
  if (actor.platformRole === 'support') {
    return `<nav aria-label="Primary"><a href="/admin?tenant=northline">Support console</a></nav>`;
  }
  return `<nav aria-label="Primary">
    <a href="/dashboard">Overview</a>
    <a href="/customers">Customers</a>
    <a href="/work-orders">Work orders</a>
    <a href="/billing">Billing</a>
    <a href="/import-export">Data</a>
  </nav>`;
}

function layout({ title, actor, body, notice = '' }) {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>${esc(title)} · RelayOps</title>
  <link rel="stylesheet" href="/assets/styles.css">
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <div class="app-shell">
    <header class="topbar">
      <a class="brand" href="${actor ? (actor.platformRole ? '/admin?tenant=northline' : '/dashboard') : '/login'}" aria-label="RelayOps home">
        <span class="brand-mark" aria-hidden="true">R</span><span>RelayOps</span>
      </a>
      ${nav(actor)}
      ${actor ? `<div class="account"><span><strong>${esc(actor.displayName)}</strong><small>${esc(actor.tenantId || 'platform')} · ${esc(actor.role)}</small></span><button class="quiet" data-action="logout" type="button">Sign out</button></div>` : ''}
    </header>
    <main id="main" tabindex="-1">
      ${notice ? `<div class="notice" role="status">${esc(notice)}</div>` : ''}
      ${body}
    </main>
  </div>
  <script src="/assets/app.js" defer></script>
</body>
</html>`;
}

function loginPage(error = '') {
  return layout({
    title: 'Sign in',
    actor: null,
    body: `<section class="login-wrap">
      <div class="login-copy">
        <p class="eyebrow">Field service operations</p>
        <h1>Keep service work moving without losing the thread.</h1>
        <p>Customers, work orders, technicians, billing and operational history stay inside the organization that owns them.</p>
        <dl class="signal-list">
          <div><dt>Tenant-aware</dt><dd>Every protected object is scoped to the active organization.</dd></div>
          <div><dt>Auditable</dt><dd>Privileged support access requires an explicit tenant context.</dd></div>
          <div><dt>Recoverable</dt><dd>Jobs, notifications and billing events are idempotent and retryable.</dd></div>
        </dl>
      </div>
      <form id="login-form" class="panel login-panel" novalidate>
        <div>
          <p class="eyebrow">RelayOps workspace</p>
          <h2>Sign in</h2>
          <p class="muted">Calibration accounts are seeded for workflow validation.</p>
        </div>
        ${error ? `<p class="form-error" role="alert">${esc(error)}</p>` : '<p class="form-error" role="alert" hidden></p>'}
        <label for="email">Email</label>
        <input id="email" name="email" type="email" autocomplete="username" value="manager@northline.test" required>
        <label for="password">Password</label>
        <input id="password" name="password" type="password" autocomplete="current-password" value="relayops-demo" required>
        <button class="primary" type="submit">Enter workspace</button>
        <p class="hint"><strong>Manager:</strong> manager@northline.test / relayops-demo<br><strong>Support:</strong> support@relayops.test / relayops-support</p>
      </form>
    </section>`,
  });
}

function dashboardPage(actor, organization, workOrders, notifications, entitlement) {
  const open = workOrders.filter((row) => !['completed', 'cancelled'].includes(row.status)).length;
  const urgent = workOrders.filter((row) => row.priority === 'urgent' || row.priority === 'high').length;
  return layout({
    title: 'Overview',
    actor,
    body: `<section class="page-head">
      <div><p class="eyebrow">${esc(organization.name)}</p><h1>Operations overview</h1><p>One view of today’s work, exceptions and account health.</p></div>
      <a class="button primary" href="/work-orders#new-order">Create work order</a>
    </section>
    <section class="metric-grid" aria-label="Operational summary">
      <article class="metric"><span>Open work</span><strong>${open}</strong><small>Across active queues</small></article>
      <article class="metric"><span>Priority attention</span><strong>${urgent}</strong><small>High or urgent</small></article>
      <article class="metric"><span>Notifications</span><strong>${notifications.length}</strong><small>For your account</small></article>
      <article class="metric"><span>Entitlement</span><strong>${esc(entitlement.status)}</strong><small>${esc(entitlement.plan)}</small></article>
    </section>
    <section class="split-grid">
      <article class="panel">
        <div class="section-title"><div><p class="eyebrow">Dispatch board</p><h2>Work requiring attention</h2></div><a href="/work-orders">View all</a></div>
        <div class="table-wrap"><table><thead><tr><th>Work order</th><th>Customer</th><th>Status</th><th>Priority</th></tr></thead><tbody>
          ${workOrders.slice(0, 6).map((row) => `<tr><td><strong>${esc(row.title)}</strong><small>${esc(row.id)}</small></td><td>${esc(row.customer_name)}</td><td>${statusBadge(row.status)}</td><td>${esc(row.priority)}</td></tr>`).join('') || '<tr><td colspan="4">No work orders.</td></tr>'}
        </tbody></table></div>
      </article>
      <aside class="panel activity-panel"><div class="section-title"><div><p class="eyebrow">Inbox</p><h2>Notifications</h2></div></div>
        ${notifications.length ? notifications.slice(0, 5).map((row) => `<article class="activity"><span class="activity-dot" aria-hidden="true"></span><div><strong>${esc(row.message)}</strong><small>${esc(row.created_at)}</small></div></article>`).join('') : '<p class="empty">Nothing new. The queue is quiet.</p>'}
      </aside>
    </section>`,
  });
}

function customersPage(actor, customers, query = '') {
  return layout({
    title: 'Customers',
    actor,
    body: `<section class="page-head"><div><p class="eyebrow">Accounts</p><h1>Customers</h1><p>Service history begins with a tenant-owned customer record.</p></div></section>
    <section class="toolbar panel">
      <form method="get" action="/customers" class="search-form"><label for="customer-search">Search customers</label><div><input id="customer-search" name="q" value="${esc(query)}" placeholder="Name or email"><button type="submit">Search</button></div></form>
      ${['manager', 'dispatcher'].includes(actor.role) ? `<button class="primary" type="button" data-toggle="customer-form">Add customer</button>` : ''}
    </section>
    ${['manager', 'dispatcher'].includes(actor.role) ? `<form id="customer-form" class="panel form-grid" hidden>
      <div class="form-heading"><h2>New customer</h2><p>Create inside ${esc(actor.tenantId)} only.</p></div>
      <label for="customer-name">Name</label><input id="customer-name" name="name" required>
      <label for="customer-email">Email</label><input id="customer-email" name="email" type="email" required>
      <label for="customer-phone">Phone</label><input id="customer-phone" name="phone">
      <div class="form-actions"><button class="primary" type="submit">Create customer</button><button type="button" data-toggle="customer-form">Cancel</button></div>
      <p class="form-error" role="alert" hidden></p>
    </form>` : ''}
    <section class="panel"><div class="table-wrap"><table><thead><tr><th>Customer</th><th>Email</th><th>Phone</th><th>Created</th></tr></thead><tbody>
      ${customers.map((row) => `<tr><td><strong>${esc(row.name)}</strong><small>${esc(row.id)}</small></td><td>${esc(row.email)}</td><td>${esc(row.phone || '—')}</td><td>${esc(row.created_at.slice(0, 10))}</td></tr>`).join('') || '<tr><td colspan="4">No customers match this search.</td></tr>'}
    </tbody></table></div></section>`,
  });
}

function workOrdersPage(actor, workOrders, customers, { status = '', query = '' } = {}) {
  return layout({
    title: 'Work orders',
    actor,
    body: `<section class="page-head"><div><p class="eyebrow">Dispatch</p><h1>Work orders</h1><p>Authoritative status transitions stay tied to the active organization.</p></div></section>
    <section class="toolbar panel">
      <form method="get" action="/work-orders" class="filter-row">
        <label for="work-search">Search</label><input id="work-search" name="q" value="${esc(query)}" placeholder="Order or customer">
        <label for="status-filter">Status</label><select id="status-filter" name="status"><option value="">All</option>${['new','scheduled','in_progress','blocked','completed','cancelled'].map((value) => `<option value="${value}" ${status === value ? 'selected' : ''}>${value.replaceAll('_',' ')}</option>`).join('')}</select>
        <button type="submit">Apply</button>
      </form>
    </section>
    ${['manager', 'dispatcher'].includes(actor.role) ? `<form id="new-order" class="panel form-grid">
      <div class="form-heading"><p class="eyebrow">New assignment</p><h2>Create work order</h2></div>
      <label for="order-customer">Customer</label><select id="order-customer" name="customerId" required>${customers.map((row) => `<option value="${esc(row.id)}">${esc(row.name)}</option>`).join('')}</select>
      <label for="order-title">Work description</label><input id="order-title" name="title" required placeholder="e.g. Replace rooftop fan motor">
      <label for="order-priority">Priority</label><select id="order-priority" name="priority"><option>normal</option><option>high</option><option>urgent</option></select>
      <div class="form-actions"><button class="primary" type="submit">Create work order</button></div><p class="form-error" role="alert" hidden></p>
    </form>` : ''}
    <section class="panel order-list" aria-label="Work order list">
      ${workOrders.map((row) => `<article class="order-row"><div><p class="eyebrow">${esc(row.customer_name)}</p><h2>${esc(row.title)}</h2><small>${esc(row.id)}</small></div><div class="order-meta">${statusBadge(row.status)}<span>${esc(row.priority)}</span><span>v${esc(row.version)}</span></div><div class="order-actions">${nextStatusButtons(row, actor)}</div></article>`).join('') || '<p class="empty">No work orders match these filters.</p>'}
    </section>`,
  });
}

function nextStatusButtons(row, actor) {
  if (!['manager', 'dispatcher', 'technician'].includes(actor.role)) return '';
  const next = { new: ['scheduled'], scheduled: ['in_progress'], in_progress: ['completed', 'blocked'], blocked: ['in_progress'] }[row.status] || [];
  return next.map((status) => `<button type="button" data-work-order="${esc(row.id)}" data-next-status="${status}">${status.replaceAll('_', ' ')}</button>`).join('');
}

function billingPage(actor, entitlement) {
  return layout({
    title: 'Billing',
    actor,
    body: `<section class="page-head"><div><p class="eyebrow">Subscription</p><h1>Billing & entitlement</h1><p>Provider events are inputs. RelayOps keeps a reconciled application entitlement as the authority used by protected operations.</p></div></section>
    <section class="split-grid">
      <article class="panel plan-card"><p class="eyebrow">Current plan</p><h2>${esc(entitlement.plan)}</h2><div class="plan-status">${statusBadge(entitlement.status)}<span>Provider version ${esc(entitlement.provider_version)}</span></div><p>Entitlement changes invalidate authorization cache state before the next protected action.</p><button class="primary" id="checkout-button" type="button">Create checkout session</button><p id="checkout-result" class="muted" role="status"></p></article>
      <article class="panel"><p class="eyebrow">Reconciliation model</p><h2>Provider state is not the gate.</h2><ol class="steps"><li>Checkout creates provider intent only.</li><li>Signed provider events are deduplicated by event ID.</li><li>Out-of-order versions are recorded but not applied.</li><li>Reconciled entitlement controls product access.</li></ol></article>
    </section>`,
  });
}

function importExportPage(actor) {
  return layout({
    title: 'Import & export',
    actor,
    body: `<section class="page-head"><div><p class="eyebrow">Data operations</p><h1>Customer import & export</h1><p>Bulk changes expose row-level outcomes and safe retry semantics inside the active tenant.</p></div><a class="button" href="/api/export">Download tenant CSV</a></section>
    <section class="split-grid">
      <form id="import-form" class="panel"><p class="eyebrow">CSV import</p><h2>Validate before retry</h2><label for="batch-key">Batch key</label><input id="batch-key" name="batchKey" value="morning-import" required><label for="csv-content">CSV content</label><textarea id="csv-content" name="csv" rows="9">name,email,phone\nOrchid Hotel,facilities@orchid.test,+1 415 555 0188\nMissing email,,+1 415 555 0199</textarea><button class="primary" type="submit">Import rows</button><p class="form-error" role="alert" hidden></p></form>
      <article class="panel"><p class="eyebrow">Row outcomes</p><h2>Latest import</h2><pre id="import-result" class="result-box" aria-live="polite">Run an import to see per-row status.</pre></article>
    </section>`,
  });
}

function adminPage(actor, targetTenant, view, auditRows) {
  const hasTenant = Boolean(targetTenant && view);
  return layout({
    title: 'Support console',
    actor,
    body: `<section class="page-head"><div><p class="eyebrow">Privileged support</p><h1>Tenant-scoped support console</h1><p>Support cannot browse globally. Every privileged read requires an explicit tenant context and leaves an audit record.</p></div></section>
    <form method="get" action="/admin" class="panel tenant-context"><label for="tenant-context">Tenant context</label><select id="tenant-context" name="tenant" required><option value="">Select tenant</option><option value="northline" ${targetTenant === 'northline' ? 'selected' : ''}>Northline Facilities</option><option value="harbor" ${targetTenant === 'harbor' ? 'selected' : ''}>Harbor Service Group</option></select><button class="primary" type="submit">Open audited context</button></form>
    ${hasTenant ? `<section class="metric-grid"><article class="metric"><span>Tenant</span><strong>${esc(view.organization.name)}</strong><small>${esc(view.organization.id)}</small></article><article class="metric"><span>Customers</span><strong>${view.customers.length}</strong></article><article class="metric"><span>Work orders</span><strong>${view.workOrders.length}</strong></article><article class="metric"><span>Audit events</span><strong>${auditRows.length}</strong></article></section>
      <section class="split-grid"><article class="panel"><h2>Tenant records</h2>${view.customers.map((row) => `<div class="compact-row"><strong>${esc(row.name)}</strong><span>${esc(row.email)}</span></div>`).join('')}</article><article class="panel"><h2>Recent privileged audit</h2>${auditRows.slice(0,8).map((row) => `<div class="compact-row"><strong>${esc(row.action)}</strong><span>${esc(row.actor_user_id)} · ${esc(row.created_at)}</span></div>`).join('')}</article></section>` : `<section class="panel empty-state"><h2>No tenant context selected</h2><p>This is intentional. Privileged support access is denied until a tenant is named explicitly.</p></section>`}`, 
  });
}

function notFoundPage() {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Not found · RelayOps</title><link rel="stylesheet" href="/assets/styles.css"></head><body><main class="not-found"><p class="eyebrow">404</p><h1>This route is outside the workspace.</h1><p>Return to your authorized RelayOps surface.</p><a class="button primary" href="/login">Go to sign in</a></main></body></html>`;
}

module.exports = {
  loginPage,
  dashboardPage,
  customersPage,
  workOrdersPage,
  billingPage,
  importExportPage,
  adminPage,
  notFoundPage,
};
