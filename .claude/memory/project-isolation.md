# Product memory isolation

- **Purpose:** Keep product knowledge out of the upstream framework repository.
- **Scope:** Product initialization, continuation, closeout and framework adoption.
- **Owner:** ATLAS maintainer
- **Source of truth:** `docs/project-local-memory-guide.md`, `scripts/project_memory.py`, `scripts/plan_project_adoption.py`
- **Last reviewed:** 2026-10-16
- **Related contracts or ADRs:** `.claude/contracts/memory-contract.md`, `.claude/contracts/workflow-contract.md`

## Invariants

- Each product owns its canonical memory and identity-bound session state.
- Toolkit location is never an implicit product-memory destination.
- Use the explicit project-root entry point for initialization, start and close.
- Adoption excludes upstream knowledge and generated views. Product repositories
  are not framework distribution sources.
- Obsidian is a generated local view, not an upstream aggregation mechanism.
- Preserve canonical user memory, edited views and ambiguous legacy state.
- Resume verification covers project identity and persisted state, not the truth
  of a caller's reported implementation or test results.

## Change triggers

Review when adding runtime hooks, automatic migration, remote persistence,
project identity changes or new storage locations.
