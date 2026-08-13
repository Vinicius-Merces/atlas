# SaaS Production Readiness Workflow

## Trigger

A feature or release introduces or materially changes user identity, protected resources, tenant data, privileged configuration, webhooks, payments/billing, third-party APIs, or other production trust boundaries.

## Objective

Deliver a SaaS change whose authentication, authorization, data isolation, secrets, integrations, financial state, observability, and recovery behavior are explicitly modeled, negatively tested, and independently reviewed before production approval.

## Inputs

- Task request, acceptance criteria, risk classification, and authority
- Current architecture, runtime/deployment model, and trust boundaries
- Authentication/session/provider configuration
- Role, permission, tenant, and ownership rules
- Database schema, policies, grants, views, and privileged functions where relevant
- Environment/secrets configuration
- Integration/payment provider contracts
- Relevant logs, metrics, traces, queues, and reconciliation mechanisms

## Sequence

1. **Map production trust boundaries**
   - Read `framework/saas-production-trust-model.md`.
   - Identify identities, resources, tenant/owner boundaries, privileged services, external providers, financial state, asynchronous processing, and recovery paths.

2. **Review authentication when applicable**
   - Run `authentication-flow-review` for sign-in, sign-up, recovery, MFA, SSO/OAuth/OIDC, session, or identity-lifecycle changes.

3. **Review authorization**
   - Run `authorization-boundary-review` for protected resources/actions, role/ownership changes, admin paths, or tenant boundaries.
   - Require direct negative tests for high-risk boundaries.

4. **Review row-level/database isolation when applicable**
   - Run `row-level-security-review` when PostgreSQL/Supabase RLS, exposed tables, service roles, views, or database policy are part of the boundary.

5. **Audit secrets and runtime configuration**
   - Run `secret-environment-audit` when credentials, signing material, database URLs, API keys, CI/CD variables, or client/server environment exposure change.

6. **Review asynchronous provider events when applicable**
   - Run `webhook-reliability-review` for inbound/outbound webhooks, provider callbacks, event retries, replay, ordering, or queue processing.

7. **Review money and entitlement state when applicable**
   - Run `payment-integration-review` for checkout, subscriptions, invoices, refunds, disputes, billing portals, or provider-driven entitlements.

8. **Review external dependency resilience**
   - Run `external-api-resilience-review` for material third-party API/SDK dependencies, especially user-facing or state-mutating calls.

9. **Validate observability and recovery**
   - Confirm authentication/security events, denied access, provider failures, retries, dead letters, reconciliation, and financial drift can be detected without exposing secrets.

10. **Run independent production-trust review**
   - A reviewer who did not solely implement the change runs `.claude/reviews/saas-production-trust-review.md`.
   - Unresolved Critical or High findings block production approval.

11. **Record evidence and continuity**
   - Record tests, provider/sandbox evidence, database policy evidence, secret-boundary evidence, review outcome, residual risk, and stable architecture/memory changes.

## Required lifecycle

1. **Understand** - Confirm product behavior, data sensitivity, identities, tenants, external providers, money/entitlement impact, authority, and acceptance criteria.
2. **Inspect** - Read canonical memory, contracts, decisions, schemas, deployment configuration, policies, integration contracts, and current runtime evidence.
3. **Plan** - Define trust boundaries, capability routing, negative tests, failure injection, review ownership, observability, and rollback/recovery.
4. **Execute** - Implement incrementally using least privilege, server-authoritative decisions, bounded retries, idempotency, and explicit configuration boundaries.
5. **Validate** - Run applicable positive, negative, cross-boundary, duplicate/retry, failure, and recovery checks.
6. **Review** - Complete independent SaaS production trust and other applicable review gates.
7. **Document** - Record evidence, decisions, residual risks, provider assumptions, and stable memory changes.
8. **Deliver** - Report Approved, Approved with conditions, Changes required, or Blocked based on actual evidence.

## Responsible agents

- `orchestrator`: classify risk, route capabilities, and enforce independent gates.
- `security-engineer`: primary trust-boundary/security owner.
- `backend-engineer`: implement server-side identity, authorization, data, and state transitions.
- `integration-engineer`: own provider/API/webhook contracts and reliability behavior.
- `platform-engineer`: own runtime environment, secret injection, deployment boundaries, and service configuration when assigned.
- `reliability-engineer`: review degradation, retries, queues, recovery, and operational evidence when material.
- `qa-engineer` or another independent reviewer: execute negative/failure-path validation and independent evidence as assigned.

## Decision points

- Which trust gates are actually applicable to the architecture?
- Is authentication provider-managed, application-managed, or mixed, and where does application responsibility begin?
- Is authorization enforced in application code, database policy, or both?
- Does tenant isolation require RLS/direct database policy evidence?
- Which configuration values may be client-visible and which are privileged secrets?
- Can webhook/provider events be duplicated, retried, reordered, or replayed?
- Which mutations require idempotency?
- What happens when an external provider times out or is unavailable?
- What state is authoritative when provider and application data disagree?
- Can the system safely recover/reconcile without inventing state?

## Validation

- Run `authentication-flow-review` for applicable identity/session changes and exercise negative authentication paths.
- Run `authorization-boundary-review` for protected actions/resources and include horizontal/vertical/cross-tenant tests as applicable.
- Run `row-level-security-review` when database row policy participates in authorization; demonstrate denied cross-owner/tenant access.
- Run `secret-environment-audit` for privileged configuration changes and inspect client/build/log exposure surfaces.
- Run `webhook-reliability-review` for event-driven integrations; test invalid signature, duplicate, retry, replay, malformed, and out-of-order behavior as applicable.
- Run `payment-integration-review` for financial/entitlement flows; test duplicate submission, ambiguous retry, failed payment, refund/cancel, and reconciliation behavior as applicable.
- Run `external-api-resilience-review` for material provider dependencies; exercise timeout, 429, 5xx, malformed response, and provider-unavailable paths where practical.
- Verify logs/metrics/traces provide enough correlation for incident investigation without leaking credentials or unnecessary sensitive data.
- Complete `saas-production-trust-review` independently for significant changes and record the outcome.
- Record commands, test identities/roles (without secrets), provider sandbox evidence, policy queries, fault-injection evidence, review outcomes, limitations, and accepted exceptions.

## Failure handling

- Stop and report Blocked when product permission/tenant policy is unknown and implementation cannot safely infer it.
- Stop production approval for proven or plausible authorization bypass, cross-tenant access, exposed privileged credentials, or duplicate irreversible financial effects.
- Do not suppress failed negative tests by changing expected outcomes without a policy decision.
- Do not acknowledge webhook/event success before durable acceptance when event loss would violate business state.
- Do not add unbounded retries to hide provider instability.
- Do not treat a checkout success redirect, client role, client tenant ID, or provider login alone as trusted authorization/business state.
- Do not self-approve unresolved Critical or High trust findings.

## Completion criteria

- Applicable trust gates are completed or explicitly marked not applicable with architectural reason.
- Authentication/session behavior is validated where present.
- Protected actions/resources have trusted authorization enforcement and negative evidence.
- Tenant/owner isolation is directly tested where present.
- Privileged secrets are not exposed to untrusted clients/artifacts/logs.
- Webhooks/provider mutations are retry-safe and observable where present.
- Payment/entitlement state is authoritative, idempotent, and reconcilable where present.
- External dependencies have bounded failure behavior.
- Independent production-trust review is Approved or Approved with resolved/accepted conditions.
- Residual risks and unavailable evidence are explicit.
