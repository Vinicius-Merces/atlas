---
name: background-job-reliability
description: "Review background jobs and queues when asynchronous work, retries, scheduling, concurrency, leases, deduplication, cancellation, dead letters, or worker recovery change, assuming duplicate delivery can occur."
---

# Background Job Reliability

## Purpose

Review asynchronous work as a failure-prone distributed system where delivery may repeat, workers may crash, ordering may vary, and durable business effects must remain safe and recoverable.

## Trigger conditions

Use when adding or changing queues, workers, scheduled jobs, delayed tasks, retries, batch processing, fan-out, synchronization jobs, leases/visibility timeouts, dead-letter handling, cancellation, or replay/reconciliation tooling.

## Inputs

- Queue/task provider semantics
- Job payload/schema and enqueue sites
- Worker implementation
- Retry/backoff/attempt configuration
- Concurrency, lease/visibility, timeout, and scheduling rules
- Idempotency/deduplication design
- Dead-letter, replay, observability, and recovery procedures

## Procedure

1. Identify the authoritative business operation represented by each job and assign a stable operation/job identity where needed.
2. Assume duplicate execution is possible unless the full provider/application contract proves otherwise; make irreversible effects idempotent or explicitly deduplicated.
3. Separate enqueue idempotency from worker/business idempotency. A unique task ID does not by itself make downstream side effects safe.
4. Classify errors as retryable, permanent, poison-data, dependency/configuration, cancellation, or ambiguous outcome.
5. Bound retries by attempts and/or duration, with backoff/jitter appropriate to the dependency; avoid infinite hot loops.
6. Configure worker deadline/lease/visibility behavior so long-running work does not create avoidable concurrent duplicates, and handle lease extension/heartbeat when supported.
7. Review concurrency races, locking/optimistic concurrency, ordering assumptions, and multiple related jobs processing simultaneously.
8. Review scheduling for duplicate enqueue, clock/time-zone/DST behavior, missed schedules, catch-up semantics, and overlapping runs.
9. Define cancellation/obsolescence behavior so stale work cannot commit after a newer operation supersedes it.
10. Route poison jobs to observable dead-letter/quarantine handling with safe replay after correction.
11. Protect queues/workers from tenant or account noisy-neighbor load using admission, concurrency, quotas, or partitioning where relevant.
12. Preserve correlation identifiers, attempts, latency, age/backlog, failure reason, and final disposition in observability.
13. Provide reconciliation for jobs whose external side effect may have succeeded even though acknowledgement/state persistence failed.

## Outputs

- Job/delivery semantics map
- Idempotency and duplicate-execution findings
- Retry/timeout/lease findings
- Ordering/concurrency/scheduling findings
- Dead-letter/replay/reconciliation findings
- Capacity/observability gaps and residual risk

## Dependencies

- Current queue/provider contract
- `external-api-resilience-review` when jobs call material providers
- `saas-multitenancy-review` for tenant-sensitive shared queues
- `observability-design` when production telemetry is incomplete

## Limitations

- Queue-provider guarantees vary and must be verified from current provider documentation.
- Exactly-once marketing language does not remove the need to reason about ambiguous business side effects.
- Does not replace workload-specific capacity testing.

## Validation

- Test duplicate delivery/execution, worker crash or timeout, retry exhaustion, poison payload, and replay paths where practical.
- Demonstrate repeated execution cannot duplicate an irreversible business effect.
- Verify dead-lettered/failed work is observable and recoverable through supported operations.
- Exercise overlapping/concurrent jobs and stale/cancelled work for high-risk state transitions.
