---
name: audit-log-design
description: "Design audit logs for consequential actions with actor, tenant, resource, action/result, correlation, sensitive-data minimization, integrity expectations, retention, access control, export, and investigation usability."
---

# Audit Log Design

## Purpose

Create trustworthy records of consequential actions that support supportability, security investigation, compliance evidence, and business traceability without turning logs into a secret dump.

## Trigger conditions

Use for admin actions, permission changes, billing/entitlement changes, data exports/deletion, account recovery, support actions, workflow approvals, regulated records, or other consequential mutations.

## Inputs

- Consequential action inventory
- Actor/service identities and tenant model
- Resource identifiers and request correlation
- Retention/privacy/compliance constraints
- Investigator/support query requirements

## Procedure

1. Define which events require audit evidence and distinguish them from noisy application telemetry.
2. Capture actor/service identity, tenant, action, target resource, timestamp, result, and correlation id using server-authoritative context.
3. Record before/after or changed fields only where useful and safe; minimize secrets, tokens, credentials, and unnecessary personal data.
4. Define append-only/tamper-evidence expectations proportional to risk.
5. Make actor impersonation/support delegation explicit so the effective actor and initiating operator remain distinguishable.
6. Define retention, access permissions, export, redaction, legal/privacy constraints, and deletion exceptions.
7. Index/query for real investigation questions without exposing broad tenant data to unauthorized operators.
8. Validate failure behavior so a logging outage does not silently erase critical evidence or create uncontrolled product outage without policy.

## Outputs

- Auditable-event matrix
- Event schema and correlation model
- Integrity/access/retention policy
- Investigation query expectations
- Failure and negative-test evidence

## Dependencies

- `authorization-boundary-review` and `saas-multitenancy-review`
- `admin-operations-surface` for support/admin actions
- `observability-design` for correlation with operational telemetry
- `privacy-impact-assessment` where retained event data is sensitive

## Limitations

Audit logs are not a substitute for metrics, traces, backups, or database history. Append-only claims require infrastructure evidence.

## Validation

- Execute representative success, denial, failed, support/impersonated, cross-tenant, and destructive actions.
- Verify actor/tenant/resource/result correlation and sensitive-data minimization.
- Confirm only authorized operators can search/export audit records.
