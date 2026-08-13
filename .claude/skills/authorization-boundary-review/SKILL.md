---
name: authorization-boundary-review
description: "Review resource and action permissions when roles, ownership, tenants, admin paths, APIs, or privileged operations change, verifying deny-by-default authorization at every trust boundary."
---

# Authorization Boundary Review

## Purpose

Verify that every protected action and resource is authorized from trusted server-side context using explicit policy rather than UI state, route visibility, or authenticated identity alone.

## Trigger conditions

Use when a change affects roles, permissions, ownership, tenancy, admin behavior, protected APIs, server actions, background jobs, impersonation, support tooling, or privileged data mutation.

## Inputs

- Resource and action inventory
- Identity/session claims and role model
- API/server action/middleware/data-access paths
- Tenant and ownership model
- Existing policies, tests, and audit events

## Dependencies

- Explicit product or policy definition for principals, resources, actions, ownership, and tenant boundaries
- Trusted authentication/session context for authenticated principals
- `row-level-security-review` when database policy participates in enforcement
- Direct server/API test access for negative authorization validation

## Procedure

1. Enumerate protected resources and meaningful actions: read, create, update, delete, export, invite, impersonate, administer, bill, and other domain operations.
2. Map principals: anonymous user, authenticated user, member, owner, administrator, support role, service identity, worker, and integration.
3. Build an access matrix from product policy rather than existing code behavior.
4. Locate the actual enforcement point for each protected operation.
5. Reject authorization that exists only in navigation, frontend conditions, client-supplied role fields, hidden buttons, or route names.
6. Prefer deny-by-default behavior and explicit grants.
7. Validate object-level authorization for identifiers supplied by users; changing an ID must not cross ownership or tenant boundaries.
8. Validate function/action-level authorization for privileged endpoints even when ordinary users cannot discover them in the UI.
9. Trace tenant identity from trusted session/service context to query/mutation enforcement. Never trust tenant IDs supplied solely by the client when a trusted source exists.
10. Review role changes, invitation acceptance, membership removal, privilege downgrade, impersonation, and stale-session behavior.
11. Review service identities and administrative bypasses for least privilege and narrow scope.
12. Test horizontal escalation, vertical escalation, cross-tenant access, stale claims, direct API invocation, parameter tampering, and alternate execution paths.
13. Map findings to current OWASP ASVS authorization/API guidance when ASVS is used as an assurance baseline.

## Outputs

- Principal-resource-action matrix
- Enforcement-point map
- Authorization findings and severity
- Cross-tenant/ownership findings
- Privileged-path findings
- Required mitigations, evidence, and residual risk

## Limitations

- Does not prove database isolation by itself; use `row-level-security-review` when RLS or database policy is part of the boundary.
- Does not replace authentication review.
- Does not infer product permissions from current implementation if policy is undocumented.

## Validation

- Execute negative authorization tests for changed or high-risk operations.
- Verify protected operations through direct server/API invocation, not only through UI behavior.
- Include at least one cross-owner or cross-tenant test where those concepts exist.
- Missing policy intent or inaccessible enforcement evidence prevents an Approved outcome for high-risk authorization changes.
