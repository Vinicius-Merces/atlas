---
name: external-api-resilience-review
description: "Review third-party API integrations when timeouts, retries, rate limits, pagination, versioning, partial failures, provider outages, or fallback behavior can affect production reliability."
---

# External API Resilience Review

## Purpose

Review outbound API dependencies as unreliable distributed-system boundaries, ensuring the application has explicit timeout, retry, idempotency, rate-limit, observability, and degradation behavior rather than assuming providers are always fast and available.

## Trigger conditions

Use when adding or changing external APIs, SDKs, provider clients, background synchronization, polling, rate-limited operations, pagination, or fallback/degradation behavior.

## Inputs

- Provider API/SDK contract and version
- Authentication and permission model
- Call sites and business criticality
- Timeout/retry configuration
- Rate-limit behavior
- Idempotency and pagination semantics
- Caching/fallback/reconciliation design
- Logs, metrics, traces, and provider request IDs

## Procedure

1. Inventory each external operation and classify it as read, mutation, asynchronous submission, polling, or reconciliation.
2. Set explicit connection/request deadlines appropriate to the user/business operation. Avoid unbounded defaults.
3. Classify failures into retryable, non-retryable, authentication/configuration, rate-limit, validation, provider-side, and ambiguous network outcomes.
4. Retry only operations safe to retry. For mutations, use provider idempotency or an application-level operation key when supported.
5. Use bounded retry budgets with backoff and jitter; avoid synchronized retry storms.
6. Respect provider rate-limit signals and design local concurrency/queue limits where burst load can exceed quotas.
7. Review pagination, cursors, filtering, and partial-page failure so synchronization does not silently skip or duplicate data.
8. Review provider API/SDK versioning and deprecation strategy. Do not float breaking versions unintentionally.
9. Decide what the product does during provider degradation: fail closed, queue, serve cached/stale data, disable a feature, or present a recoverable error.
10. Preserve provider request/correlation IDs and enough context for troubleshooting without logging secrets or excessive personal data.
11. Review circuit-breaking or admission-control behavior when repeated dependency failure can consume local capacity.
12. For eventually consistent syncs, define authoritative source, conflict resolution, replay, and reconciliation.
13. Test malformed responses, schema additions, missing optional fields, timeouts, 429s, 5xx errors, network resets, and partial failures.

## Outputs

- External dependency inventory
- Failure classification
- Timeout/retry/idempotency findings
- Rate-limit and concurrency findings
- Versioning/pagination findings
- Degradation and reconciliation model
- Required mitigations and residual risk

## Limitations

- Provider-specific contracts override generic assumptions.
- Does not recommend retries merely to hide persistent provider failures.
- Does not treat SDK defaults as sufficient evidence of production-safe behavior.

## Validation

- Inject or simulate timeout, 429, 5xx, network ambiguity, malformed response, and provider-unavailable cases where practical.
- Verify mutation retries cannot duplicate side effects.
- Confirm retry budgets remain bounded and observable.
- Demonstrate the intended user/system degradation path when the provider is unavailable.
