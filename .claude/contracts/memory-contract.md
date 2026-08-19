# Memory Contract

Memory stores stable project knowledge shared across agents.

Memory is not a transcript archive. It is a governed set of reusable claims whose authority, freshness, and replacement relationships can be inspected.

## Required properties

Every canonical memory document should identify:

- Purpose
- Scope
- Source of truth
- Owner
- Last reviewed or last verified date
- Related contracts or ADRs

For memory whose correctness can expire or drift materially, also define one of:

- next review date;
- review cadence;
- expiration/TTL rule;
- explicit event that requires revalidation.

## Claim-level metadata

When a memory document contains claims with different sources, confidence, or lifetimes, record claim-level metadata where practical:

- provenance/source
- confidence or validation status
- `last_verified_at`
- freshness/expiry rule when time-sensitive
- `supersedes` relationship when replacing older guidance
- `conflicts_with` relationship when a contradiction is unresolved

Do not add metadata ceremony to every sentence. Use claim-level fields where they change how a future agent should trust or refresh the information.

## Confidence guidance

Confidence must describe evidence quality, not model certainty.

Example categories:

- **verified**: directly supported by the current authoritative source or runtime evidence;
- **reviewed**: accepted by the owner/reviewer but not freshly rechecked against runtime state;
- **provisional**: useful working context that still requires verification before consequential use;
- **stale**: known to require refresh and must not be treated as current truth.

Unverified assumptions do not become durable memory merely by assigning them a confidence label.

## Suitable content

- Business rules
- Architecture
- Data ownership
- Brand guidance
- Integration contracts
- Security policies
- Stable product constraints
- Validated operational constraints
- Provider/runtime decisions that remain reusable

## Unsuitable content

- Secrets
- Temporary debugging findings
- Unverified assumptions presented as fact
- One-off task instructions
- Sensitive production data
- Generated content without review
- Raw conversation history with no stable reusable claim
- Volatile external facts without a freshness/revalidation rule

## Update rules

- Update memory when the source of truth changes.
- Revalidate time-sensitive memory according to its cadence/expiry rule.
- Record material architecture changes in an ADR.
- Remove or supersede stale guidance rather than accumulating contradictions.
- Prefer one canonical document per topic.
- Preserve provenance when consolidating or superseding memory.
- Do not silently rewrite disputed claims; record conflict and route for review.

## Retrieval rules

A consuming agent should prefer:

1. current authoritative source/runtime evidence;
2. verified canonical memory;
3. reviewed memory whose freshness window remains valid;
4. provisional memory only as a hypothesis requiring verification.

Stale or contradicted memory must not override fresher repository/runtime evidence.

## Memory quality signals

ATLAS may measure memory health using signals such as:

- stale-item rate
- overdue-review rate
- source/provenance coverage
- unresolved contradiction count
- superseded-item leakage into active context
- repeated rediscovery caused by missing durable memory
- stale-hit rate: retrieved memory later shown to be outdated during task execution

Metrics are diagnostic evidence, not a reason to retain low-value memory.
