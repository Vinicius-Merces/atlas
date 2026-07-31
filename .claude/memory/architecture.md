# ATLAS Architecture Memory

- **Purpose:** Preserve the stable runtime and source-of-truth architecture.
- **Scope:** ATLAS framework repository and supported runtime adapters.
- **Owner:** Governance steward
- **Source of truth:** `framework/architecture.md`, `compatibility/core-contracts.json`, and runtime declarations under `adapters/`
- **Last reviewed:** 2026-07-30
- **Related contracts or ADRs:** `.claude/contracts/`, `framework/adr/ADR-001-separate-knowledge-from-execution.md`

## Stable constraints

- Claude Code is the canonical runtime and its implementation lives in
  `.claude/`.
- Codex is a beta-supported compatibility runtime under `adapters/codex/`.
- Contracts, memory, framework models, documentation, schemas, and templates
  are shared sources; adapters translate runtime form without redefining them.
- Canonical agent definitions live only in `.claude/agents/`.
- Codex catalogs and machine-readable maps are generated from
  `.claude/registry.json` and must pass drift detection.
- Gemini and Cursor remain experimental and are not stabilization priorities.

## Change triggers

Review this memory when canonical paths, runtime support classification,
contract semantics, or adapter ownership changes.
