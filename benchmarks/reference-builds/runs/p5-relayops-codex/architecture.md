# RelayOps architecture and operational contract

## Product boundary

RelayOps is a dependency-free Node SSR application backed by SQLite. The run models two different service organizations and five operational roles. The browser receives an opaque HttpOnly session cookie; tenant and role are reloaded from authoritative membership state on every request.

The visual thesis is an **operational relay board**: mineral surfaces, dense tables, clear semantic states and a relay line that connects work-order transitions. The authenticated interface avoids marketing-page composition and generic card-grid dashboards.

## Authority map

| State | Authority | Isolation/recovery rule |
|---|---|---|
| Identity/session | `users`, hashed `sessions` | revocation and membership reload on every request |
| Tenant role | `memberships` | never accepted from client or cached session claims |
| Customers/orders | tenant-scoped composite keys | every lookup/mutation includes trusted tenant context |
| Attachments | private SQLite objects + metadata | never served as static files; read/write reauthorizes tenant and order |
| Search | tenant predicate inside SQL | no global result fetch followed by client filtering |
| Cache | `(tenant, scope, key, authz_version)` | role/entitlement revocation invalidates or version-rejects stale values |
| Jobs | durable tenant-bearing row and unique operation key | worker revalidates tenant resource and mutable authorization |
| Notifications/email | tenant recipient derivation + idempotent outbox/job | provider acceptance is separate from authoritative event |
| Billing | provider projection plus application entitlement | checkout return never grants access; signed events reconcile entitlement |
| Support | global support role plus explicit target header/reason | no implicit tenant; all permitted/denied actions are audited |
| Import/export | tenant-owned import job/query | row-level partial result, source hash, safe replay, tenant-scoped CSV |

SQLite provides transactional local authority but is not presented as PostgreSQL RLS or horizontally scaled production storage. A persistent, multi-instance production rollout would replace it with shared PostgreSQL, preserve the composite tenant contracts, migrate in expand/backfill/contract phases and keep old/new application versions compatible during rollout.

## Failure and recovery

- Jobs use bounded attempts and terminal failure; recovery is explicit replay after the provider is healthy.
- Duplicate job delivery creates one effect using a tenant/operation/effect unique key.
- Provider webhook event IDs are durable, signatures are verified against raw payload, and stale provider timestamps are ignored.
- Reconciliation maps the latest provider projection into versioned application entitlements and clears entitlement cache.
- Backups require SQLite online backup or application-quiesced snapshot plus attachment/object verification. Restore is followed by integrity checks and provider/job reconciliation before traffic resumes.
- Consequential requests emit correlation IDs and structured redacted logs; audit records retain actor, tenant, action, target, result, reason and correlation.

## Deployment truth

The runner supports the campaign's ephemeral controlled HTTPS preview. That preview is not production and cannot prove shared database topology, persistent secrets, email/payment live credentials, backup automation, domain ownership or SLA. `saas-production-config` must remain non-pass while claimable production is disabled by the campaign.
