# Context efficiency

- **Purpose:** Preserve context budget and freshness invariants.
- **Scope:** Derived context packs and runtime execution planning.
- **Owner:** ATLAS maintainer
- **Source of truth:** `docs/context-pack-guide.md`, `docs/context-efficiency-plan.md`, `scripts/build_context_pack.py`, `scripts/validate_context_pack.py`
- **Last reviewed:** 2026-10-16
- **Related contracts or ADRs:** `.claude/contracts/memory-contract.md`, `.claude/contracts/workflow-contract.md`

## Invariants

- The complete rendered pack must fit its declared global character budget.
- Canonical instructions and task constraints are never silently cut to fit.
- Optional omitted and truncated context must be disclosed and reviewed.
- Verify pack integrity and every included source hash before planning; rebuild
  after changes. Verification does not establish semantic completeness.
- Place stable canonical context before task-specific content. A stable prefix
  hash supports diagnosis but is not evidence of a provider cache hit.
- Legacy context without a manifest is an explicitly unverified draft.
- Character counts, token counts, provider cache reuse and local extraction reuse
  are distinct measurements. No savings percentage has been established.

## Change triggers

Review when introducing semantic retrieval, a local extraction cache, provider
adapters, compaction or changes to manifest compatibility.
