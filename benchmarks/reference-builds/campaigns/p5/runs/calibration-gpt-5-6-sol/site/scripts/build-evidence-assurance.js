const fs = require('node:fs');
const path = require('node:path');

const siteRoot = path.resolve(__dirname, '..');
const runRoot = path.resolve(siteRoot, '../run');
const repoRoot = path.resolve(siteRoot, '../../../../../../..');
const browserRoot = path.join(runRoot, 'evidence', 'public-browser');
const browserSummaryPath = path.join(browserRoot, 'browser-summary.json');
const deploymentPath = path.join(runRoot, 'deployment.json');

function rel(file) {
  return path.relative(repoRoot, file).split(path.sep).join('/');
}
function must(file) {
  if (!fs.existsSync(file)) throw new Error(`Missing evidence ${file}`);
  return file;
}

const browser = JSON.parse(fs.readFileSync(must(browserSummaryPath), 'utf8'));
const deployment = JSON.parse(fs.readFileSync(must(deploymentPath), 'utf8'));
const screenshots = fs.readdirSync(path.join(browserRoot, 'screenshots'))
  .filter((name) => name.endsWith('.png'))
  .sort()
  .map((name) => rel(path.join(browserRoot, 'screenshots', name)));
const recoveryJobs = rel(path.join(runRoot, 'evidence', 'tenant-cache-jobs.json'));
const recoveryBilling = rel(path.join(runRoot, 'evidence', 'billing-entitlements.json'));
const httpSecurity = rel(path.join(runRoot, 'evidence', 'http-security.json'));
const environmentManifest = rel(path.join(runRoot, 'environment-capability.json'));
const browserSummaryRef = rel(browserSummaryPath);
const deploymentRef = rel(deploymentPath);
const evidenceReferences = [...new Set([environmentManifest, browserSummaryRef, deploymentRef, recoveryJobs, recoveryBilling, httpSecurity, ...screenshots])];

const missing = evidenceReferences.filter((value) => !fs.existsSync(path.join(repoRoot, value)));
if (missing.length) throw new Error(`Missing indexed evidence: ${missing.join(', ')}`);

const notFound = browser.seo_not_found || {};
const manifest = {
  version: 2,
  environment_manifest: environmentManifest,
  evidence_references: evidenceReferences,
  browser: {
    source: 'campaign-portable',
    summary: browserSummaryRef,
    screenshots,
  },
  non_text_contrast: {
    minimum_required: 3.0,
    samples: []
  },
  seo_not_found: [{
    route: notFound.route || '/__atlas_reference_build_missing__',
    status: Number(notFound.status || 0),
    robots: Array.isArray(notFound.robots) ? notFound.robots : [],
    canonical: notFound.canonical || null,
    evidence_ref: browserSummaryRef,
  }],
  visual_regression: {
    mode: 'capture-only',
    baseline_root: null,
    diff_report: null,
  },
  recovery_claims: [
    {
      claim: 'Notification jobs retry after provider failure without uncontrolled duplicate delivery.',
      advertised: true,
      implementation_ref: rel(path.join(siteRoot, 'src', 'store.js')),
      evidence_ref: recoveryJobs,
    },
    {
      claim: 'Billing entitlement reconciliation rejects stale and duplicate provider events.',
      advertised: true,
      implementation_ref: rel(path.join(siteRoot, 'src', 'store.js')),
      evidence_ref: recoveryBilling,
    },
  ],
  mutable_cache: [
    { route: '/dashboard', shared: false, max_age_seconds: 0, freshness_budget_seconds: 0, evidence_ref: httpSecurity },
    { route: '/customers', shared: false, max_age_seconds: 0, freshness_budget_seconds: 0, evidence_ref: httpSecurity },
    { route: '/work-orders', shared: false, max_age_seconds: 0, freshness_budget_seconds: 0, evidence_ref: httpSecurity },
  ],
  deployment: {
    status: 'public-https',
    deployment_class: 'controlled-preview',
    claimable_production: false,
    url: deployment.url,
    evidence_ref: deploymentRef,
  },
};

fs.writeFileSync(path.join(runRoot, 'evidence-assurance.json'), JSON.stringify(manifest, null, 2) + '\n');
console.log(JSON.stringify({ output: rel(path.join(runRoot, 'evidence-assurance.json')), screenshot_count: screenshots.length, deployment: deployment.url }, null, 2));
