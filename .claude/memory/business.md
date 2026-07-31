# ATLAS Business Memory

- **Purpose:** Preserve the product intent and permanent delivery constraints.
- **Scope:** ATLAS framework product and its manual distribution workflow.
- **Owner:** Product architect
- **Source of truth:** `README.md`, `framework/principles.md`, and `docs/installation.md`
- **Last reviewed:** 2026-07-30
- **Related contracts or ADRs:** `.claude/contracts/`, `framework/adr/ADR-001-separate-knowledge-from-execution.md`

## Product purpose

ATLAS turns a repository into portable engineering memory and governed
execution infrastructure so work can continue across sessions, machines, and
AI runtimes without relying on chat history.

## Permanent constraints

- Repository knowledge and contracts are authoritative.
- Delivery must remain incremental, reversible, auditable, and usable without
  mandatory external services.
- The owner applies release updates manually.
- Incremental packages expose `.claude/` payloads as
  `CLAUDE-DIRECTORY/`, while the installed repository retains `.claude/`.
- Deletions are explicit; absence from a patch never authorizes removal.

## Change triggers

Review this memory when product scope, supported delivery modes, or the manual
deployment contract changes.
