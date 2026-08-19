---
name: memory-freshness-audit
description: "Assess persistent memory ownership, source, age, and reliability."
---

# Memory Freshness Audit

## Purpose

Assess whether persistent project memory is still authoritative enough to guide current work, including provenance, ownership, age, confidence, review cadence, supersession, contradiction, and stale-context risk.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints
- Canonical memory documents and index
- Current repository/runtime/source-of-truth evidence
- ADRs, contracts, provider/platform evidence, and continuity artifacts relevant to the topic
- Ownership and review-date metadata

## Procedure

1. Inventory the memory topics relevant to the requested domain instead of auditing the entire corpus by default.
2. For each active topic, identify the authoritative source, owner, last-reviewed/last-verified date, and expected freshness rule.
3. Classify each material claim as verified, reviewed, provisional, stale, or unknown based on evidence quality and freshness, not model confidence.
4. Compare time-sensitive claims with current authoritative evidence. External platform/provider behavior, pricing, limits, APIs, deployment constraints, and policies require stronger freshness scrutiny than long-lived design principles.
5. Identify memory with no usable provenance or with a source that no longer exists or is no longer authoritative.
6. Identify overdue review/TTL/expiry conditions. Expired memory becomes a verification requirement, not automatically current truth.
7. Trace `supersedes` relationships or equivalent replacement notes and identify superseded guidance still being loaded/referenced as active context.
8. Identify unresolved contradictions among memory, ADRs, contracts, repository state, runtime state, and current authoritative sources.
9. Measure stale-hit evidence when available: memory retrieved as current but later disproved during implementation/audit.
10. Identify repeated rediscovery caused by missing durable memory only when the rediscovered information is stable and reusable enough to store.
11. Propose bounded updates through `memory-update-proposal`; do not silently rewrite disputed or stale memory during the audit.
12. Record residual uncertainty and the evidence required to restore a claim to verified/reviewed status.

## Output

- Audited memory topics
- Source/provenance map
- Ownership and review status
- Claim confidence/validation classification
- Overdue/expired memory
- Superseded-memory leakage
- Contradictions and unresolved authority
- Stale-hit findings when measurable
- Missing durable-memory opportunities
- Proposed refresh/removal/supersession actions
- Validation status and residual risk

## Trigger conditions

Use when project memory may be outdated, conflicting, weakly sourced, inherited across sessions/runtimes, or relied upon for consequential implementation/release decisions.

## Dependencies

- `.claude/contracts/memory-contract.md`
- `framework/memory-engine.md`
- `source-of-truth-validation`
- `memory-drift-analysis` when repository/runtime divergence is material
- `memory-update-proposal` for reviewable changes

## Limitations

- Fresh metadata does not prove a claim is correct; current authoritative evidence wins.
- Does not grant authority to rewrite disputed memory or waive review gates.
- Does not turn temporary debugging observations or volatile facts into durable memory merely to improve coverage metrics.
- Missing or inaccessible evidence must be reported, not guessed.

## Validation

- Re-check a representative set of important claims against the current authoritative source/runtime evidence.
- Confirm stale/superseded claims are not being presented as active verified context.
- Confirm contradictions name both competing sources and the unresolved authority when applicable.
- Ensure proposed updates preserve provenance and do not introduce secrets or sensitive production data.
- Report overdue, stale, provisional, and unknown states explicitly rather than collapsing them into "current".
