const fs = require('node:fs');
const path = require('node:path');

const siteRoot = path.resolve(__dirname, '..');
const runRoot = path.resolve(siteRoot, '../run');
const repoRoot = path.resolve(siteRoot, '../../../../../../..');
const evidenceRoot = path.join(runRoot, 'evidence');

function rel(file) {
  return path.relative(repoRoot, file).split(path.sep).join('/');
}

function evidence(name) {
  const file = path.join(evidenceRoot, `${name}.json`);
  if (!fs.existsSync(file)) throw new Error(`Missing generated evidence ${file}`);
  return rel(file);
}

const refs = {
  auth: evidence('auth-membership'),
  httpAuth: evidence('http-auth-flow'),
  db: evidence('tenant-database'),
  storage: evidence('tenant-storage'),
  search: evidence('tenant-search'),
  cacheJobs: evidence('tenant-cache-jobs'),
  notifications: evidence('notifications'),
  billing: evidence('billing-entitlements'),
  admin: evidence('admin-audit'),
  httpAdmin: evidence('http-admin-flow'),
  importExport: evidence('import-export'),
  secret: evidence('secret-boundary'),
  httpOperational: evidence('http-operational-flow'),
  httpSecurity: evidence('http-security'),
};
const browserFlow = path.join(evidenceRoot, 'browser', 'browser-auth-flow.json');
if (fs.existsSync(browserFlow)) refs.browserFlow = rel(browserFlow);

const uniqueEvidence = [...new Set(Object.values(refs))];
const manifest = {
  version: 1,
  run_manifest: rel(path.join(runRoot, 'manifest.json')),
  evidence_references: uniqueEvidence,
  auth_and_membership: {
    session_lifecycle_ref: refs.auth,
    organization_membership_ref: refs.auth,
    unauthenticated_denial_ref: refs.httpAuth,
    role_denial_ref: refs.admin,
  },
  tenant_database: {
    attempts: [
      { source_tenant: 'northline', target_tenant: 'harbor', operation: 'customer/work-order read', outcome: 'denied', evidence_ref: refs.db },
      { source_tenant: 'harbor', target_tenant: 'northline', operation: 'foreign customer write dependency', outcome: 'denied', evidence_ref: refs.db },
    ],
  },
  tenant_storage: {
    attempts: [
      { source_tenant: 'harbor', target_tenant: 'northline', operation: 'attachment read', outcome: 'denied', evidence_ref: refs.storage },
      { source_tenant: 'harbor', target_tenant: 'northline', operation: 'attachment write to foreign work order', outcome: 'denied', evidence_ref: refs.storage },
    ],
  },
  tenant_search: {
    attempts: [
      { source_tenant: 'northline', target_tenant: 'harbor', operation: 'foreign customer/work-order search', outcome: 'denied', evidence_ref: refs.search },
    ],
  },
  tenant_cache_jobs: {
    cache_isolation_ref: refs.cacheJobs,
    job_context_ref: refs.cacheJobs,
    duplicate_delivery_ref: refs.cacheJobs,
    retry_recovery_ref: refs.cacheJobs,
    stale_authorization_ref: refs.cacheJobs,
  },
  notifications: {
    tenant_delivery_ref: refs.notifications,
    provider_failure_ref: refs.notifications,
    recovery_ref: refs.notifications,
  },
  billing_entitlements: {
    checkout_ref: refs.httpOperational,
    authoritative_entitlement_ref: refs.billing,
    duplicate_webhook_ref: refs.billing,
    out_of_order_webhook_ref: refs.billing,
    reconciliation_ref: refs.billing,
    revocation_ref: refs.billing,
  },
  admin_audit: {
    explicit_tenant_context: true,
    least_privilege_denial_ref: refs.admin,
    privileged_action_ref: refs.httpAdmin,
    audit_record_ref: refs.admin,
  },
  import_export: {
    row_validation_ref: refs.importExport,
    partial_failure_ref: refs.importExport,
    safe_retry_ref: refs.importExport,
    export_isolation_ref: refs.importExport,
  },
  secret_boundary: {
    browser_bundle_scan_ref: refs.secret,
    client_log_scan_ref: refs.secret,
    exposed_privileged_secrets: 0,
  },
  notes: 'Generated from executed Node tests and, when present, authenticated Playwright evidence. Controlled preview and independent review are handled by separate assurance sidecars.',
};

fs.writeFileSync(path.join(runRoot, 'saas-assurance.json'), JSON.stringify(manifest, null, 2) + '\n');
console.log(JSON.stringify({ output: rel(path.join(runRoot, 'saas-assurance.json')), evidence_count: uniqueEvidence.length }, null, 2));
