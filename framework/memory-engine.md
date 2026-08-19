# Memory Engine

The Memory Engine stores stable project knowledge and makes it available to agents without embedding that knowledge inside execution prompts.

## Objectives

- Preserve validated project knowledge.
- Reduce repeated discovery.
- Prevent contradictory guidance.
- Keep agents focused on execution.
- Make context updates traceable.
- Prevent stale memory from overriding fresher repository/runtime evidence.
- Measure memory quality instead of equating memory volume with memory usefulness.

## Memory resolution flow

```text
Task
  ↓
Identify affected domains
  ↓
Load bounded relevant memory
  ↓
Check provenance, freshness and conflicts
  ↓
Compare with current source/runtime evidence
  ↓
Merge with ADRs, contracts and rules
  ↓
Exclude stale/superseded claims
  ↓
Provide bounded context to agents
```

## Memory characteristics

A valid memory item should be:

- Stable enough to reuse
- Specific enough to guide decisions
- Traceable to a source of truth
- Owned by a person, role, or system
- Reviewable
- Fresh enough for its consequence
- Explicit about unresolved contradiction when one exists
- Free from secrets

## Freshness model

Not all memory ages at the same rate.

Examples:

- brand principles may be long-lived and event-reviewed;
- architecture decisions may remain valid until superseded by an ADR/change;
- provider/runtime configuration may need periodic or release-triggered revalidation;
- deployment limits, pricing, external APIs, policies, and platform behavior may require short review windows.

Each time-sensitive memory topic should define a review cadence, next-review date, expiry/TTL, or explicit revalidation event.

Expiration does not delete knowledge automatically. It changes the claim from trusted current context into evidence that requires verification.

## Confidence and provenance

Confidence reflects evidence quality, not how persuasive the text sounds.

Prefer claims that are:

1. verified against authoritative current evidence;
2. reviewed and still inside their freshness window;
3. provisional only as hypotheses to validate.

Keep source/provenance close enough to the claim that a future agent can re-check it without rediscovering the entire project.

## Supersession and conflict

When guidance changes:

- prefer explicit `supersedes` relationships or a clear replacement note;
- stop loading superseded material as active instruction;
- preserve historical provenance when it matters for audit/continuity;
- use `conflicts_with` or a contradiction record when two live sources disagree and authority is unresolved;
- never resolve a material contradiction by silently choosing the more convenient memory.

## Canonicality

One canonical memory document should exist per topic. Related documents may reference it, but must not redefine the same rules independently.

Project briefs, session packets, summaries, and Obsidian navigation may point to canonical memory but do not become parallel sources of truth merely because they are easier to retrieve.

## Retrieval discipline

Memory retrieval should optimize for relevance and decision value, not maximum recall.

Do not load the entire memory corpus for every task.

Prefer:

- affected domains;
- current canonical topic documents;
- decisions/contracts linked to the task;
- recent continuity records only when they materially explain repository state.

Avoid carrying obsolete implementation details into unrelated work.

## Memory health metrics

The Memory Engine may report:

- number/rate of stale active items
- overdue reviews
- provenance/source coverage
- unresolved contradictions
- superseded items still referenced by active context
- stale-hit rate during real work
- repeated rediscovery caused by missing durable knowledge
- context footprint for common task classes

These metrics are used to improve memory quality and retrieval discipline. They must not incentivize retaining more memory than the project needs.

## Update policy

Memory updates should normally be proposed or traced through the canonical memory workflow rather than silently appended during unrelated implementation.

A project change is not complete merely because code changed. If it invalidates durable architecture, integration, product, security, deployment, or operating knowledge, the affected canonical memory must be reconciled or explicitly marked pending.
