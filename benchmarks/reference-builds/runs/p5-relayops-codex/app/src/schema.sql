PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS organizations (
  id TEXT PRIMARY KEY, slug TEXT NOT NULL UNIQUE, name TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('active','suspended')), created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY, email TEXT NOT NULL UNIQUE, name TEXT NOT NULL,
  password_hash TEXT NOT NULL, global_role TEXT CHECK(global_role IN ('support') OR global_role IS NULL), created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS memberships (
  tenant_id TEXT NOT NULL, user_id TEXT NOT NULL, role TEXT NOT NULL CHECK(role IN ('manager','dispatcher','technician','billing')),
  status TEXT NOT NULL CHECK(status IN ('active','revoked')), authz_version INTEGER NOT NULL DEFAULT 1,
  PRIMARY KEY(tenant_id,user_id), FOREIGN KEY(tenant_id) REFERENCES organizations(id), FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS invites (
  id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, email TEXT NOT NULL, role TEXT NOT NULL,
  token_hash TEXT NOT NULL UNIQUE, expires_at TEXT NOT NULL, used_at TEXT,
  FOREIGN KEY(tenant_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS sessions (
  token_hash TEXT PRIMARY KEY, user_id TEXT NOT NULL, tenant_id TEXT, expires_at TEXT NOT NULL,
  revoked_at TEXT, created_at TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS customers (
  id TEXT NOT NULL, tenant_id TEXT NOT NULL, external_ref TEXT, name TEXT NOT NULL, email TEXT NOT NULL,
  phone TEXT NOT NULL, site_address TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('active','inactive')),
  version INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
  PRIMARY KEY(tenant_id,id), UNIQUE(tenant_id,email), UNIQUE(tenant_id,external_ref), FOREIGN KEY(tenant_id) REFERENCES organizations(id)
);
CREATE INDEX IF NOT EXISTS customers_search ON customers(tenant_id,name,email,status);
CREATE TABLE IF NOT EXISTS work_orders (
  id TEXT NOT NULL, tenant_id TEXT NOT NULL, customer_id TEXT NOT NULL, title TEXT NOT NULL, description TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('new','scheduled','in_progress','blocked','completed','cancelled')),
  priority TEXT NOT NULL CHECK(priority IN ('low','normal','high','urgent')), assigned_user_id TEXT,
  scheduled_at TEXT, version INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
  PRIMARY KEY(tenant_id,id), FOREIGN KEY(tenant_id,customer_id) REFERENCES customers(tenant_id,id), FOREIGN KEY(assigned_user_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS work_orders_search ON work_orders(tenant_id,status,priority,title,updated_at);
CREATE TABLE IF NOT EXISTS work_order_events (
  id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, work_order_id TEXT NOT NULL, actor_user_id TEXT NOT NULL,
  from_status TEXT, to_status TEXT NOT NULL, created_at TEXT NOT NULL,
  FOREIGN KEY(tenant_id,work_order_id) REFERENCES work_orders(tenant_id,id)
);
CREATE TABLE IF NOT EXISTS attachments (
  id TEXT NOT NULL, tenant_id TEXT NOT NULL, work_order_id TEXT NOT NULL, storage_key TEXT NOT NULL,
  filename TEXT NOT NULL, mime TEXT NOT NULL, size INTEGER NOT NULL CHECK(size <= 262144), sha256 TEXT NOT NULL,
  body_base64 TEXT NOT NULL, created_by TEXT NOT NULL, created_at TEXT NOT NULL,
  PRIMARY KEY(tenant_id,id), UNIQUE(tenant_id,storage_key), FOREIGN KEY(tenant_id,work_order_id) REFERENCES work_orders(tenant_id,id)
);
CREATE TABLE IF NOT EXISTS notifications (
  id TEXT NOT NULL, tenant_id TEXT NOT NULL, user_id TEXT NOT NULL, kind TEXT NOT NULL, title TEXT NOT NULL,
  body TEXT NOT NULL, dedupe_key TEXT NOT NULL, read_at TEXT, created_at TEXT NOT NULL,
  PRIMARY KEY(tenant_id,id), UNIQUE(tenant_id,dedupe_key), FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS email_outbox (
  id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, user_id TEXT NOT NULL, to_email TEXT NOT NULL, event_key TEXT NOT NULL,
  subject TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('pending','retry','delivered','failed')),
  attempts INTEGER NOT NULL DEFAULT 0, max_attempts INTEGER NOT NULL DEFAULT 3, next_attempt_at TEXT,
  last_error TEXT, provider_id TEXT, created_at TEXT NOT NULL, UNIQUE(tenant_id,event_key)
);
CREATE TABLE IF NOT EXISTS jobs (
  id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, type TEXT NOT NULL, operation_key TEXT NOT NULL, payload_json TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('queued','running','retry','completed','failed','denied')),
  attempts INTEGER NOT NULL DEFAULT 0, max_attempts INTEGER NOT NULL DEFAULT 3, authz_version INTEGER,
  last_error TEXT, run_after TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, UNIQUE(tenant_id,type,operation_key)
);
CREATE TABLE IF NOT EXISTS job_effects (
  tenant_id TEXT NOT NULL, operation_key TEXT NOT NULL, effect_type TEXT NOT NULL, effect_id TEXT NOT NULL, created_at TEXT NOT NULL,
  PRIMARY KEY(tenant_id,operation_key,effect_type)
);
CREATE TABLE IF NOT EXISTS cache_entries (
  tenant_id TEXT NOT NULL, scope TEXT NOT NULL, cache_key TEXT NOT NULL, value_json TEXT NOT NULL,
  authz_version INTEGER NOT NULL, expires_at TEXT NOT NULL, PRIMARY KEY(tenant_id,scope,cache_key)
);
CREATE TABLE IF NOT EXISTS subscriptions (
  tenant_id TEXT PRIMARY KEY, provider_subscription_id TEXT, provider_status TEXT NOT NULL,
  app_status TEXT NOT NULL, plan TEXT NOT NULL, last_provider_ts INTEGER NOT NULL DEFAULT 0,
  entitlement_version INTEGER NOT NULL DEFAULT 1, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS entitlements (
  tenant_id TEXT NOT NULL, feature TEXT NOT NULL, enabled INTEGER NOT NULL CHECK(enabled IN (0,1)),
  source TEXT NOT NULL, reason TEXT NOT NULL, version INTEGER NOT NULL, confirmed_at TEXT NOT NULL,
  PRIMARY KEY(tenant_id,feature)
);
CREATE TABLE IF NOT EXISTS webhook_events (
  event_id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, event_type TEXT NOT NULL, provider_ts INTEGER NOT NULL,
  payload_hash TEXT NOT NULL, disposition TEXT NOT NULL, received_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS checkout_sessions (
  id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, plan TEXT NOT NULL, status TEXT NOT NULL,
  idempotency_key TEXT NOT NULL, created_at TEXT NOT NULL, UNIQUE(tenant_id,idempotency_key)
);
CREATE TABLE IF NOT EXISTS audit_log (
  id TEXT PRIMARY KEY, tenant_id TEXT, actor_user_id TEXT, effective_role TEXT NOT NULL, action TEXT NOT NULL,
  resource TEXT NOT NULL, resource_id TEXT, result TEXT NOT NULL, reason TEXT, correlation_id TEXT NOT NULL,
  details_json TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS audit_tenant_time ON audit_log(tenant_id,created_at DESC);
CREATE TABLE IF NOT EXISTS imports (
  id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, operation_key TEXT NOT NULL, source_hash TEXT NOT NULL,
  status TEXT NOT NULL, created_count INTEGER NOT NULL, failed_count INTEGER NOT NULL, report_json TEXT NOT NULL,
  created_at TEXT NOT NULL, UNIQUE(tenant_id,operation_key)
);
CREATE TABLE IF NOT EXISTS import_rows (
  import_id TEXT NOT NULL, tenant_id TEXT NOT NULL, row_number INTEGER NOT NULL, row_hash TEXT NOT NULL,
  status TEXT NOT NULL, entity_id TEXT, error TEXT, PRIMARY KEY(import_id,row_number)
);
CREATE TABLE IF NOT EXISTS rate_events (
  actor_key TEXT NOT NULL, scope TEXT NOT NULL, occurred_at INTEGER NOT NULL
);
