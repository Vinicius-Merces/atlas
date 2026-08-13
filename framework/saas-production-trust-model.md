# SaaS Production Trust Model

## Purpose

ATLAS uses the SaaS Production Trust Model to distinguish a feature that works in development from a service that can safely hold user identity, tenant data, secrets, integrations, and money in production.

The model is vendor-neutral. Provider-specific controls may strengthen or implement the model, but they do not replace the underlying trust requirements.

For web application security verification, use the current stable OWASP Application Security Verification Standard as a recognized external baseline when the project requires a formal assurance reference. ATLAS remains responsible for mapping only the requirements that actually apply to the system under review.

## Core principle

Production trust is an end-to-end property:

```text
identity
  ↓
authentication
  ↓
authorization
  ↓
data isolation
  ↓
secret/config boundaries
  ↓
integration reliability
  ↓
financial/state consistency
  ↓
observability + recovery
  ↓
independent production-trust review
```

A secure login screen does not compensate for missing object authorization. Correct API authorization does not compensate for a service key shipped to the browser. Valid webhook signatures do not compensate for duplicate side effects. A successful checkout redirect does not prove payment or entitlement state.

## Trust domains

### 1. Identity and authentication

Production authentication must cover the complete lifecycle, not only credential submission:

- sign-up and sign-in;
- federation/SSO/OAuth/OIDC when enabled;
- session creation, renewal, revocation, and logout;
- passwordless/OTP/magic-link behavior;
- MFA and privileged step-up where required;
- recovery and contact-change flows;
- account linking and identity-provider namespace;
- disabled/deleted users and stale sessions;
- abuse controls and security observability.

Use `authentication-flow-review` for material changes.

### 2. Authorization boundaries

Authorization must be enforced at trusted execution boundaries for both resources and actions.

Never treat these as sufficient authorization controls by themselves:

- a hidden button;
- a missing navigation link;
- a client-side role check;
- a route name;
- possession of an object ID;
- successful authentication;
- a tenant ID supplied only by the client.

Use `authorization-boundary-review` for object, action, role, tenant, admin, and service-identity permissions.

### 3. Data isolation and RLS

When database row policy is part of the trust boundary, policy must survive bypass of ordinary application UI and query composition.

For PostgreSQL/Supabase-style RLS:

- RLS enablement is explicit;
- default-deny behavior is understood;
- grants and policies are both reviewed;
- `USING` and `WITH CHECK` semantics match the operation;
- anonymous/null identity behavior is explicit;
- user-editable metadata is not trusted for privileged authorization;
- service-role/owner/BYPASSRLS/security-definer paths are treated as privileged bypasses;
- views and functions are reviewed for invoker/definer behavior;
- cross-tenant negative tests are required for tenant-isolated systems.

Use `row-level-security-review`.

### 4. Secrets and environment configuration

Configuration must be classified by exposure, not by naming convention.

A value is not safe merely because it is stored in an environment variable. The important questions are:

- can the client bundle see it?
- can build output or source maps expose it?
- can logs/telemetry print it?
- can preview environments access production value?
- is its permission scope wider than needed?
- can it be revoked and rotated?
- is there evidence of historic source-control exposure?

Use `secret-environment-audit`.

### 5. Webhook/event trust

Treat webhook delivery as an adversarial at-least-once network boundary unless the provider contract proves stronger semantics.

Required considerations:

- sender authenticity and signature verification;
- raw-body requirements;
- timestamp/replay controls;
- duplicate delivery and business idempotency;
- out-of-order events;
- concurrent related events;
- bounded acknowledgement latency;
- durable acceptance before acknowledgement when loss matters;
- retries, dead-letter/recovery, and replay tooling;
- event-schema evolution;
- observability.

Use `webhook-reliability-review`.

### 6. Payments and billing

Money and entitlement flows are distributed state machines.

The application must not infer durable payment/entitlement success solely from browser navigation or optimistic client state.

Review:

- server-authoritative price/product validation;
- mutation idempotency;
- duplicate submission and ambiguous network outcomes;
- provider webhook synchronization;
- subscription lifecycle and failed renewal;
- refunds/disputes/cancellation/reactivation;
- customer/admin billing authorization;
- sandbox/live separation;
- provider/app reconciliation.

Use `payment-integration-review`.

### 7. External API resilience

External APIs are dependencies with independent latency, quotas, versions, and failure modes.

Every production-critical integration needs explicit behavior for:

- connection/request deadlines;
- retryable versus non-retryable errors;
- idempotent mutation retries;
- retry budget/backoff/jitter;
- rate limits and local concurrency;
- pagination and partial failure;
- API/SDK versioning;
- provider request IDs;
- degraded operation;
- replay/reconciliation.

Use `external-api-resilience-review`.

## Production trust gates

A material SaaS change is not production-ready while any applicable gate lacks evidence:

1. **Identity gate** - authentication lifecycle and session behavior are known and tested.
2. **Authorization gate** - protected resources/actions have trusted enforcement and negative tests.
3. **Isolation gate** - tenant/owner data boundaries have direct negative evidence; database policy is reviewed when applicable.
4. **Secrets gate** - privileged credentials are server-only, scoped, non-logged, and revocable.
5. **Integration gate** - retries, duplicates, rate limits, timeouts, and provider outage behavior are explicit.
6. **Financial gate** - money/entitlement state is idempotent, authoritative, and reconcilable when payments exist.
7. **Observability gate** - security/integration failures can be detected and investigated without leaking secrets.
8. **Recovery gate** - failed asynchronous operations can be replayed/reconciled safely where business state would otherwise drift.
9. **Independent review gate** - significant production-trust changes receive review by someone other than the sole implementer.

## Block conditions

Block production approval when evidence shows or cannot rule out a material risk such as:

- authentication assertion accepted without required integrity/issuer/audience/session checks;
- horizontal or vertical authorization bypass;
- cross-tenant data access;
- missing RLS on an intentionally exposed table where RLS is the security boundary;
- privileged/service secret exposed to an untrusted client or repository artifact;
- webhook/payment retries causing duplicate irreversible side effects;
- client-controlled price/entitlement/role accepted as authoritative;
- unbounded external API calls or retry storms that can exhaust service capacity;
- unresolved Critical or High production-trust review finding.

## Proportionality

Not every project uses every gate. A public static site does not need RLS or payment review. A single-tenant internal tool may have different isolation requirements than a multi-tenant SaaS.

Mark a capability `not applicable` only with a short reason tied to actual architecture. Do not skip a gate merely because the provider is managed or because a framework/library claims secure defaults.

## Evidence standard

Prefer direct evidence over configuration claims:

- negative tests;
- role/tenant-separated requests;
- database policy queries;
- built-client artifact inspection;
- sandbox provider events;
- duplicate/retry/reordering simulations;
- timeout/rate-limit fault injection;
- logs/metrics without secret disclosure;
- reconciliation output.

The implementing agent may produce evidence, but it must not be the sole approver for significant trust-boundary changes.
