---
name: webhook-reliability-review
description: "Review inbound or outbound webhooks when event delivery, signatures, retries, ordering, deduplication, async processing, or replay behavior changes."
---

# Webhook Reliability Review

## Purpose

Review webhooks as an at-least-once, adversarial network boundary that must authenticate the sender, tolerate retries and duplicates, survive reordering, and separate acknowledgement from durable processing when appropriate.

## Trigger conditions

Use when adding or changing webhook endpoints, event destinations, provider callbacks, event consumers, retries, queues, signature verification, or delivery state.

## Inputs

- Provider/event contract and signing scheme
- Endpoint implementation and raw request handling
- Event identity, ordering, and versioning model
- Queue/job/storage architecture
- Retry and dead-letter behavior
- Logs, metrics, dashboards, and replay tooling

## Dependencies

- Authoritative provider event/signature/delivery documentation
- Stable event or business-operation identity for deduplication/idempotency where available
- Durable storage or processing boundary when event loss would violate business state
- `secret-environment-audit` when signing secrets or callback credentials change
- `authorization-boundary-review` when authenticated events can trigger privileged business actions

## Procedure

1. Identify sender, receiver, transport, event identity, signature scheme, and trust boundary.
2. Verify the signature against the exact bytes/headers required by the provider before trusting event contents. Do not parse/re-serialize a body if the signing scheme requires the raw payload.
3. Validate timestamp/replay protections when supported and define an acceptable clock-skew window.
4. Persist or otherwise atomically record a stable event/delivery identifier before side effects when duplicates are possible.
5. Make handlers idempotent at the business-operation level. Deduplicating an HTTP request is not enough if the same logical event can arrive under different delivery attempts.
6. Assume retries and duplicate events can occur. Confirm retryable failures produce retryable responses and permanent invalid events do not create endless hot loops.
7. Assume events can arrive out of order unless the provider explicitly guarantees otherwise. Reconcile against authoritative current state when order matters.
8. Keep acknowledgement latency bounded. Offload slow work to durable processing when available, but do not acknowledge before the event is durably accepted if loss would matter.
9. Review concurrency races when two related events process simultaneously.
10. Version event schemas and tolerate additive fields; reject or quarantine truly incompatible payloads deliberately.
11. Protect endpoints from unbounded payloads, unexpected methods/content types, denial scenarios, and secret leakage in logs.
12. Provide observability for accepted, rejected, duplicated, failed, retried, dead-lettered, and replayed events.
13. Provide a controlled replay/reconciliation path for operational recovery.

## Outputs

- Webhook trust and delivery model
- Signature/replay findings
- Idempotency/deduplication findings
- Ordering/concurrency findings
- Retry/queue/replay findings
- Observability and recovery gaps
- Required mitigations and residual risk

## Limitations

- Provider delivery semantics are authoritative and must be verified from provider documentation.
- Does not assume HTTP 2xx means downstream processing succeeded unless durable acceptance is established.
- Does not treat signature verification as authorization for every business action contained in an event.

## Validation

- Test valid signature, invalid signature, stale/replayed delivery, duplicate delivery, handler retry, and malformed payload paths.
- Test out-of-order related events where ordering affects state.
- Demonstrate that duplicate/retried events cannot duplicate irreversible business side effects.
- Verify failed events are observable and recoverable without manual database surgery where feasible.
