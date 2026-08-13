---
name: saas-multitenancy-review
description: "Review SaaS multitenancy when tenant identity, pooled/siloed resources, quotas, storage, caches, jobs, search, exports, or operational isolation change, verifying cross-tenant safety and noisy-neighbor controls."
---

# SaaS Multitenancy Review

## Purpose

Review the complete tenant boundary across application, data, compute, storage, caches, queues, search, observability, and operations instead of treating database authorization as the entire multitenancy model.

## Trigger conditions

Use when adding tenants/workspaces/organizations, changing pooled/silo/bridge architecture, tenant routing or identity, shared data/storage/search/cache/queue resources, quotas, per-tenant plans, tenant migration/export/deletion, support impersonation, or noisy-neighbor controls.

## Inputs

- Tenant identity and membership model
- Resource partitioning/isolation architecture
- Authorization and RLS policies
- Database, object storage, cache, queue/job, search/index, and analytics paths
- Quota/tier/rate-limit design
- Tenant-aware logs, metrics, billing/usage, export, deletion, and migration behavior

## Procedure

1. Define what a tenant is, where trusted tenant identity originates, and how it propagates through synchronous and asynchronous work.
2. Classify each material resource as pooled, siloed, bridge/hybrid, or intentionally global and document the isolation mechanism.
3. Verify cross-tenant access is prevented independently of user-controlled tenant IDs, URLs, cache keys, object paths, job payloads, or search filters.
4. Compose with `authorization-boundary-review` and `row-level-security-review` for application/database enforcement; multitenancy review extends beyond those boundaries.
5. Inspect object storage, file exports, search indexes, vector stores, caches, queues, scheduled jobs, webhooks, analytics, backups, and logs for tenant leakage paths.
6. Review tenant-aware cache and deduplication keys, background-job payloads, idempotency keys, and reconciliation so one tenant cannot collide with another.
7. Evaluate noisy-neighbor risk across CPU, memory, connections, queue depth, API/provider quota, database workload, cache capacity, and expensive reports/exports.
8. Review quotas, throttling, concurrency limits, per-tenant admission control, and plan/tier enforcement from trusted server state.
9. Verify support/admin impersonation, break-glass access, tenant migration, merge/split, offboarding, export, deletion, and legal-retention paths.
10. Ensure observability can attribute load, failures, cost, and abuse to a tenant without exposing another tenant's sensitive data.
11. Test tenant change/removal while sessions, jobs, cache entries, invites, and provider callbacks are still in flight.
12. Document accepted shared blast radius and the recovery strategy when a pooled dependency fails.

## Outputs

- Tenant/resource isolation matrix
- Cross-tenant leakage findings
- Pooled/silo/bridge architecture findings
- Noisy-neighbor and quota findings
- Tenant lifecycle/operations findings
- Required mitigations, direct tests, and residual risk

## Dependencies

- `authorization-boundary-review`
- `row-level-security-review` when database row policy is used
- `background-job-reliability` for material asynchronous tenant work
- `cache-strategy-assessment` for tenant-sensitive caching

## Limitations

- No single isolation pattern is universally correct; compliance, workload, cost, and product tiers affect architecture.
- Passing RLS tests does not prove storage, cache, queue, search, export, or observability isolation.
- Does not replace provider-specific tenancy controls when managed services impose additional boundaries.

## Validation

- Execute representative cross-tenant negative tests across each changed resource class.
- Demonstrate tenant identity cannot be switched through client-supplied identifiers alone.
- Exercise quota/noisy-neighbor behavior for at least one expensive path when shared resources are material.
- Verify offboarding/removal prevents stale sessions/jobs/caches from regaining access and record any unavailable evidence.
