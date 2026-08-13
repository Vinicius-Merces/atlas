---
name: admin-operations-surface
description: "Design internal admin and support surfaces for privileged operations, covering role boundaries, tenant context, search, impersonation, dangerous actions, approval/confirmation, audit evidence, support workflows, break-glass access, and prevention of accidental cross-customer impact."
---

# Admin Operations Surface

## Purpose

Design privileged operational tooling that helps support and administrators resolve real problems without bypassing the application's trust model or making cross-customer mistakes easy.

## Trigger conditions

Use for admin dashboards, support consoles, back-office CRUD, user/tenant lookup, entitlement adjustment, refunds, impersonation, data repair, moderation, or break-glass tooling.

## Inputs

- Admin/support roles and responsibilities
- Privileged actions and affected resources
- Tenant/customer context model
- Approval, audit, and support requirements
- Emergency/break-glass policy

## Procedure

1. Inventory privileged actions and assign least-privilege roles rather than one universal admin bit.
2. Keep tenant/customer context prominent, explicit, and server-enforced throughout navigation and mutations.
3. Separate read-only investigation from state-changing operations.
4. Require stronger confirmation, reason capture, dual control, or re-authentication for high-impact actions according to risk.
5. If impersonation is necessary, make entry/exit unmistakable, time-bound, scoped, auditable, and incapable of hiding the initiating operator.
6. Design search and bulk operations to avoid accidental broad tenant scope.
7. Route destructive/financial/security actions through domain services instead of direct database edits where business invariants matter.
8. Define break-glass access, alerts, expiration, review, and credential handling.
9. Ensure every consequential action emits appropriate audit evidence.
10. Test support failure paths and accessibility because internal tools still cause production-impacting mistakes.

## Outputs

- Admin role/action matrix
- Tenant-context and privileged UX design
- Confirmation/approval/break-glass policy
- Audit and support workflow mapping
- Negative-path evidence

## Dependencies

- `authorization-boundary-review`
- `audit-log-design`
- `payment-integration-review` for financial operations
- `authentication-flow-review` for re-authentication/privileged sessions

## Limitations

Internal-only does not mean low-risk. Direct database access may still be necessary for emergencies, but should not become the default product workflow.

## Validation

- Test role escalation, cross-tenant search/action, dangerous confirmation, impersonation entry/exit, break-glass expiry, and audit evidence.
- Verify privileged routes/actions cannot be reached by ordinary users through direct requests.
