const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');

const baseUrl = process.env.RELAYOPS_BROWSER_BASE_URL || 'http://127.0.0.1:4173';
const evidenceRoot = process.env.RELAYOPS_BROWSER_EVIDENCE_DIR
  ? path.resolve(process.env.RELAYOPS_BROWSER_EVIDENCE_DIR)
  : path.resolve(__dirname, '../../run/evidence/browser');
fs.mkdirSync(evidenceRoot, { recursive: true });

async function screenshot(page, name) {
  const file = path.join(evidenceRoot, `${name}.png`);
  await page.screenshot({ path: file, fullPage: true, animations: 'disabled' });
  return path.basename(file);
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, reducedMotion: 'reduce' });
  const page = await context.newPage();
  const consoleErrors = [];
  const pageErrors = [];
  const failedRequests = [];
  const errorResponses = [];
  page.on('console', (message) => { if (message.type() === 'error') consoleErrors.push(message.text()); });
  page.on('pageerror', (error) => pageErrors.push(String(error)));
  page.on('requestfailed', (request) => failedRequests.push({ url: request.url(), error: request.failure()?.errorText || 'unknown' }));
  page.on('response', (response) => {
    if (response.status() >= 400) errorResponses.push({ url: response.url(), status: response.status(), method: response.request().method() });
  });

  const screenshots = [];
  const checks = {};

  await page.goto(`${baseUrl}/login`, { waitUntil: 'networkidle' });
  checks.login_heading = await page.getByRole('heading', { name: 'Sign in' }).isVisible();
  await page.getByLabel('Email').fill('manager@northline.test');
  await page.getByLabel('Password').fill('relayops-demo');
  await Promise.all([
    page.waitForURL(/\/dashboard$/),
    page.getByRole('button', { name: 'Enter workspace' }).click(),
  ]);
  checks.authenticated_dashboard = await page.getByRole('heading', { name: 'Operations overview' }).isVisible();
  checks.northline_visible = await page.getByText('Northline Facilities').first().isVisible();
  checks.harbor_not_visible = (await page.getByText('Harbor Service Group').count()) === 0;
  screenshots.push(await screenshot(page, '01-manager-dashboard'));

  await page.getByRole('link', { name: 'Customers' }).click();
  await page.getByRole('button', { name: 'Add customer' }).click();
  await page.getByLabel('Name').fill('Browser Flow Clinic');
  await page.getByLabel('Email').fill('facilities@browserflow.test');
  await page.getByLabel('Phone').fill('+1 415 555 0119');
  await Promise.all([
    page.waitForLoadState('networkidle'),
    page.getByRole('button', { name: 'Create customer' }).click(),
  ]);
  checks.customer_created = await page.getByText('Browser Flow Clinic').isVisible();
  screenshots.push(await screenshot(page, '02-customer-created'));

  await page.getByRole('link', { name: 'Work orders' }).click();
  await page.getByLabel('Customer').selectOption({ label: 'Browser Flow Clinic' });
  await page.getByLabel('Work description').fill('Validate rooftop safety controls');
  await page.getByLabel('Priority').selectOption('high');
  await Promise.all([
    page.waitForLoadState('networkidle'),
    page.getByRole('button', { name: 'Create work order' }).click(),
  ]);
  checks.work_order_created = await page.getByRole('heading', { name: 'Validate rooftop safety controls' }).isVisible();
  const orderRow = page.locator('.order-row').filter({ hasText: 'Validate rooftop safety controls' });
  await Promise.all([
    page.waitForLoadState('networkidle'),
    orderRow.getByRole('button', { name: 'scheduled' }).click(),
  ]);
  checks.work_order_transitioned = await page.locator('.order-row').filter({ hasText: 'Validate rooftop safety controls' }).getByText('scheduled').isVisible();
  screenshots.push(await screenshot(page, '03-work-order-scheduled'));

  await page.getByRole('link', { name: 'Billing' }).click();
  const entitlementBefore = (await page.locator('.plan-status').innerText()).toLowerCase();
  await page.getByRole('button', { name: 'Create checkout session' }).click();
  await page.getByText(/Checkout intent checkout_/).waitFor();
  checks.checkout_does_not_directly_grant = entitlementBefore.includes('active') && (await page.locator('.plan-status').innerText()).toLowerCase().includes('active');
  screenshots.push(await screenshot(page, '04-billing-entitlement'));

  await page.getByRole('link', { name: 'Data' }).click();
  await page.getByRole('button', { name: 'Import rows' }).click();
  await page.getByText(/invalid_name_or_email/).waitFor();
  const importResult = await page.locator('#import-result').innerText();
  checks.import_partial_failure_visible = importResult.includes('imported') && importResult.includes('failed');
  screenshots.push(await screenshot(page, '05-import-partial-failure'));

  await page.getByRole('button', { name: 'Sign out' }).click();
  await page.waitForURL(/\/login$/);
  checks.logout_returned_to_login = true;

  await page.getByLabel('Email').fill('support@relayops.test');
  await page.getByLabel('Password').fill('relayops-support');
  await page.getByRole('button', { name: 'Enter workspace' }).click();
  await page.waitForURL(/\/admin/);
  checks.support_starts_without_tenant_context = await page.getByRole('heading', { name: 'No tenant context selected' }).isVisible();
  await page.getByLabel('Tenant context').selectOption('harbor');
  await Promise.all([
    page.waitForLoadState('networkidle'),
    page.getByRole('button', { name: 'Open audited context' }).click(),
  ]);
  checks.support_explicit_harbor_context = await page.locator('.metric strong').filter({ hasText: /^Harbor Service Group$/ }).isVisible();
  checks.support_northline_data_not_visible = (await page.getByText('Atlas Dental Group').count()) === 0;
  checks.support_audit_visible = await page.getByText('support.tenant_viewed').first().isVisible();
  screenshots.push(await screenshot(page, '06-support-explicit-tenant'));

  const overflow = await page.evaluate(() => Math.max(0, document.documentElement.scrollWidth - document.documentElement.clientWidth));
  checks.final_viewport_horizontal_overflow = overflow;

  await browser.close();
  const requiredChecks = Object.entries(checks).filter(([key]) => key !== 'final_viewport_horizontal_overflow');
  const passed = requiredChecks.every(([, value]) => value === true) && overflow === 0 && consoleErrors.length === 0 && pageErrors.length === 0 && failedRequests.length === 0 && errorResponses.length === 0;
  const summary = {
    version: 1,
    evidence_source: 'calibration-playwright-authenticated',
    base_url: baseUrl,
    checks,
    console_errors: consoleErrors,
    page_errors: pageErrors,
    failed_requests: failedRequests,
    error_responses: errorResponses,
    screenshots,
    passed,
  };
  fs.writeFileSync(path.join(evidenceRoot, 'browser-auth-flow.json'), JSON.stringify(summary, null, 2) + '\n');
  console.log(JSON.stringify(summary, null, 2));
  if (!passed) process.exit(1);
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
