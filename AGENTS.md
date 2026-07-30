# ATLAS Instructions for Codex

This repository uses ATLAS as its engineering operating framework.

## Canonical sources

- Framework: `framework/`
- Contracts: `.claude/contracts/`
- Memory: `.claude/memory/`
- Agents: `.claude/agents/`
- Skills: `.claude/skills/`
- Workflows: `.claude/workflows/`
- Reviews: `.claude/reviews/`
- Commands: `.claude/commands/`
- Codex adapter: `adapters/codex/`

## Codex behavior

1. Read relevant project memory before planning.
2. Use canonical ATLAS contracts.
3. Follow the closest mapped Codex workflow.
4. Preserve agent responsibility and review gates.
5. Report execution evidence using `adapters/codex/instructions/execution-evidence.md`.
6. Do not fork project knowledge by runtime.
7. Record runtime limitations explicitly.

## Preferred entry points

- Plan: `adapters/codex/commands/atlas-plan.md`
- Implement: `adapters/codex/commands/atlas-implement.md`
- Review: `adapters/codex/commands/atlas-review.md`
- Release: `adapters/codex/commands/atlas-release.md`
