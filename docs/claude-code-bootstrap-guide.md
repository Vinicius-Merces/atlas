# Claude Code Bootstrap Guide

Start from the repository root and read the project continuity artifacts before
planning. Project memory and decisions remain shared with Codex through the
repository.

## Bootstrap sequence

1. Read `AGENTS.md`.
2. Read `.claude/registry.json`.
3. Load relevant `.claude/memory/` documents and accepted ADRs.
4. Follow the closest `.claude/command` and workflow.
5. Preserve contracts and required review gates.
6. Record validation, risks, documentation, and continuity evidence.

Canonical agents live in `.claude/agents/`; no parallel root agent directory is
supported.
