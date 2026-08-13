---
name: rate-limit-abuse-control
description: "Design abuse and resource-consumption controls for public or expensive operations, covering actor and resource keys, rate and concurrency limits, payload bounds, OTP/recovery abuse, uploads, provider spend, failure responses, bypass identities, and observability."
---

# Rate Limit & Abuse Control

## Purpose

Protect availability, cost, identity flows, and expensive product operations with limits derived from business behavior and abuse paths rather than a single global requests-per-minute number.

## Trigger conditions

Use for public APIs, authentication/recovery/OTP, AI generation, search, exports, uploads, webhooks, expensive reports, third-party provider calls, or endpoints with material compute/storage/spend impact.

## Inputs

- Operation cost and expected legitimate usage
- Actor identities: IP, session, user, tenant, API key, resource
- Payload and concurrency dimensions
- Provider quotas/cost model
- Known abuse/fraud patterns and recovery requirements

## Procedure

1. Inventory resource dimensions: frequency, concurrency, payload size, result size, CPU, memory, storage, provider spend, and irreversible actions.
2. Choose keys that reflect the actual actor/resource boundary; avoid IP-only identity where shared networks or authenticated actors make it misleading.
3. Define burst and sustained limits plus concurrency/admission control where parallel work is the risk.
4. Bound request fields, array sizes, upload sizes, pagination limits, export scope, and generated output where applicable.
5. Apply stricter controls to OTP, recovery, invite, messaging, billing, and other abuse-amplifying operations.
6. Define trusted service/admin bypasses narrowly and make them observable.
7. Return stable retry/error semantics without revealing sensitive account existence or internal capacity details.
8. Add provider spending limits/alerts where external cost cannot be bounded entirely in application logic.
9. Test distributed/concurrent behavior and graceful degradation when the limiter store is unavailable.

## Outputs

- Resource/abuse inventory
- Limit key and policy matrix
- Payload/concurrency bounds
- Bypass and degradation policy
- Metrics, alerts, and negative-test evidence

## Dependencies

- `authentication-flow-review` for identity abuse surfaces
- `external-api-resilience-review` for downstream quotas
- `file-upload-storage-design` for upload limits
- `observability-design` for limit/abuse telemetry

## Limitations

Rate limiting alone is not bot, fraud, or DDoS prevention. Exact thresholds require production usage evidence and may need tuning.

## Validation

- Exercise burst, sustained, concurrent, oversized, anonymous, authenticated, and bypass cases.
- Verify limits do not cross tenant/user keys incorrectly.
- Confirm failure semantics and limiter-store degradation behavior.
- Inspect metrics for allowed, limited, bypassed, and provider-quota events.
