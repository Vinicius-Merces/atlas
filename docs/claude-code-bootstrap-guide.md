# Claude Code Bootstrap Guide

Start from the repository root. Claude Code loads `CLAUDE.md`, which imports
the shared `AGENTS.md` instructions. Read project continuity artifacts before
planning; project memory and decisions remain shared with Codex through the
repository.

## Bootstrap sequence

1. Read `AGENTS.md`.
2. Read `.claude/registry.json`.
3. Load relevant `.claude/memory/` documents and accepted ADRs.
4. Follow the closest `.claude/commands/` entry point and workflow.
5. Preserve contracts and required review gates.
6. Record validation, risks, documentation, and continuity evidence.

Canonical agents live in `.claude/agents/`, and native skills live under
`.claude/skills/*/SKILL.md`. Markdown files under `.claude/workflows/` and
`.claude/reviews/` are canonical ATLAS procedures that Claude interprets for
the task; their presence alone is not execution evidence.
