---
name: row-level-security-review
description: "Review PostgreSQL/Supabase row-level security when exposed tables, tenancy, ownership policies, service roles, views, or database authorization change, verifying default-deny data isolation."
---

# Row-Level Security Review

## Purpose

Review row-level authorization as a database security boundary, especially for browser-accessible APIs and multi-tenant systems, and verify that policies enforce the intended ownership and tenant model even when application code is bypassed.

## Trigger conditions

Use when PostgreSQL RLS, Supabase Data API access, exposed schemas, tenant isolation, ownership policies, service-role access, security-definer functions, or views are added or changed.

## Inputs

- Tables, schemas, views, functions, roles, grants, and RLS policies
- Authentication/JWT claim model
- Tenant/ownership rules
- Client and server database access paths
- Migration SQL and tests

## Procedure

1. Inventory tables/views reachable by untrusted or user-context clients.
2. Confirm RLS is enabled on every table where row policy is part of the security model. For exposed Supabase schemas, treat missing RLS as a release blocker unless access is intentionally impossible by another enforced boundary.
3. Confirm grants and policies both follow least privilege; RLS does not replace inappropriate table/role grants.
4. Verify default-deny behavior for roles/actions without an explicit policy.
5. Review `SELECT`, `INSERT`, `UPDATE`, and `DELETE` separately. Verify `USING` and `WITH CHECK` express the intended read/write rules.
6. Verify unauthenticated behavior explicitly. Do not rely on ambiguous null comparisons for identity functions.
7. Treat user-editable JWT/user metadata as untrusted authorization input. Prefer server-controlled claims or authoritative database relationships.
8. Review service-role, secret-key, owner, `BYPASSRLS`, and security-definer paths as privileged bypasses. They must not be exposed to clients and must be narrowly scoped.
9. Review views for invoker/definer behavior and whether they preserve or bypass underlying row policies.
10. Review functions for `SECURITY DEFINER`, search path, and privilege escalation risk.
11. Check indexes and query shape for policy predicates on large or frequently scanned tables so security controls do not become an avoidable availability problem.
12. Test same-user, other-user, same-tenant, other-tenant, anonymous, privileged-service, and stale/changed membership cases as applicable.
13. Validate raw SQL migrations, not only dashboard state.

## Outputs

- Exposed data-surface inventory
- Table/action/policy matrix
- Privileged bypass inventory
- Cross-tenant/ownership findings
- Performance findings tied to policy predicates
- Required mitigations, tests, and residual risk

## Limitations

- RLS is one layer of authorization and does not replace API/action authorization.
- Does not assume Supabase; use PostgreSQL semantics as the portable baseline and provider-specific checks only when present.
- Does not consider a dashboard checkbox sufficient evidence without policy and grant inspection.

## Validation

- Execute queries under representative unprivileged roles/claims when safe.
- Demonstrate denied access for cross-owner or cross-tenant cases.
- Verify privileged service paths are unavailable to client bundles and public configuration.
- Inspect migrations/schema state for RLS enablement, policies, grants, views, and privileged functions.
