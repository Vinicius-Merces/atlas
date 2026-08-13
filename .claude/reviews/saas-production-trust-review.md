# SaaS Production Trust Review Gate

## Scope

Evaluate a significant SaaS change for production trust across identity, authorization, tenant/data isolation, secrets/configuration, asynchronous integrations, payments/entitlements, external dependency resilience, observability, and recovery.

This gate is independent from functional correctness. A feature can pass happy-path tests and still fail production trust.

## Required evidence

- Request, acceptance criteria, risk classification, and affected paths
- Trust-boundary or architecture context
- Authentication/session evidence when applicable
- Authorization matrix and negative tests when applicable
- Database/RLS policy evidence when applicable
- Secret/environment exposure evidence when applicable
- Webhook/API/provider contract and failure-path evidence when applicable
- Payment/billing sandbox/reconciliation evidence when applicable
- Logs, metrics, traces, or recovery evidence appropriate to the change
- Implementation diff, relevant tests, contracts, and known limitations

Missing mandatory trust-boundary evidence prevents an Approved outcome.

## Review questions

### Identity and session

- Are all authentication entry points and callbacks known?
- Are identity assertions, sessions, recovery, MFA/step-up, and account-linking behavior appropriate to the risk?
- Can stale/disabled identities or replayed/invalid assertions retain access?

### Authorization

- What resources/actions require permission, and where is each decision enforced?
- Can a user cross ownership, role, or tenant boundaries by changing identifiers or calling endpoints directly?
- Are privileged/admin/service actions separately authorized?
- Is authorization based on trusted server-side identity/policy rather than client state?

### Data isolation / RLS

- Is database row policy part of the security boundary?
- Are exposed tables, grants, policies, views, and privileged bypasses correctly scoped?
- Is cross-tenant/other-owner denial demonstrated directly?
- Are user-editable claims prevented from granting privileged access?

### Secrets and environment

- Which configuration values are public and which are privileged?
- Can any privileged secret reach a browser bundle, source map, log, build artifact, preview deployment, or repository history?
- Are production credentials scoped, separated, revocable, and rotatable?

### Webhooks and asynchronous events

- Is sender authenticity verified correctly?
- Can duplicate, retried, replayed, malformed, concurrent, or out-of-order events produce unsafe business effects?
- Is acceptance durable before acknowledgement when loss matters?
- Are failed events observable and recoverable?

### Payments and entitlements

- Are price/product/currency/discount/entitlement decisions server-authoritative?
- Are financial mutations retry-safe and idempotent?
- Can browser navigation grant entitlement without authoritative provider state?
- Are refunds, failed renewals, cancellation, disputes, and reconciliation covered?
- Are test/sandbox and live resources separated?

### External APIs

- Are deadlines/timeouts explicit?
- Are retries bounded, classified, and safe for the operation?
- Are rate limits, pagination, provider versions, partial failures, and degradation behavior handled?
- Can dependency failure exhaust local resources or create duplicate state?

### Observability and recovery

- Can denied access, auth anomalies, provider failures, duplicate events, retry exhaustion, payment drift, and reconciliation failures be detected?
- Are correlation IDs/provider request IDs retained where useful?
- Are secrets and unnecessary sensitive data excluded from logs?
- Is there a safe replay/reconciliation path for state that can drift?

## Findings

Record each finding with:

- severity
- observed evidence
- affected trust boundary/path/state
- exploit or failure scenario
- impact on confidentiality, integrity, availability, financial correctness, or tenant isolation
- required remediation
- verification method

State `No findings` only after every applicable trust domain and required evidence source has been inspected.

## Severity

Use `.claude/contracts/review-contract.md`:

- Critical
- High
- Medium
- Low
- Note

Authorization bypass, cross-tenant data access, exposed privileged credentials, or duplicate irreversible payment effects are normally blocking until evidence proves the issue resolved or non-applicable.

## Required actions

For every finding, identify the correction, decision, or evidence required and how it will be verified. Critical or High findings must be resolved or explicitly governed before approval. Missing mandatory negative tests, provider contract evidence, RLS evidence, or secret-boundary evidence must be listed as required action rather than assumed safe.

## Outcome

Record exactly one outcome after required evidence and mandatory validation are complete:

- Approved
- Approved with conditions
- Changes required
- Blocked

The sole implementing agent may provide evidence and remediation but must not be the only approver of its own significant production-trust work.
