# ATLAS Contradiction Register

- **Purpose:** Make material conflicts between canonical sources explicit.
- **Scope:** Runtime, contract, memory, documentation, and release claims.
- **Owner:** Knowledge contradiction reviewer
- **Source of truth:** `adapters/shared/source-of-truth-manifest.json` and accepted reconciliation evidence
- **Last reviewed:** 2026-07-30
- **Related contracts or ADRs:** `.claude/contracts/memory-contract.md`, `framework/adr/ADR-001-separate-knowledge-from-execution.md`

## Open contradictions

None recorded.

## Resolved contradictions

### Legacy agent path

- Conflict: agent files existed in root `agents/` while contracts and runtime
  documentation declared `.claude/agents/` canonical.
- Resolution: definitions were consolidated into `.claude/agents/`; registry,
  Codex maps, and drift validation now resolve that path.
- Resolution date: 2026-07-30
- Reopen when: a runtime or package introduces a second agent source.
