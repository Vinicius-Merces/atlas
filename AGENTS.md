# ATLAS Instructions for Codex

This repository uses ATLAS as its engineering operating framework.

## Canonical sources

- Framework: `framework/`
- Registry: `.claude/registry.json`
- Contracts: `.claude/contracts/`
- Memory: `.claude/memory/`
- Agents: `.claude/agents/`
- Skills: `.claude/skills/`
- Workflows: `.claude/workflows/`
- Reviews: `.claude/reviews/`
- Commands: `.claude/commands/`
- Codex adapter: `adapters/codex/`
- Operating guide: `docs/operations-guide.md`

## Codex behavior

1. Read relevant project memory before planning.
2. Use canonical ATLAS contracts.
3. Follow the closest mapped Codex workflow.
4. Preserve agent responsibility and review gates.
5. Report execution evidence using `adapters/codex/instructions/execution-evidence.md`.
6. Do not fork project knowledge by runtime.
7. Record runtime limitations explicitly.
8. Apply `docs/project-delivery-feedback.md`: save validated batches, track exact
   remaining work, and distinguish implementation, validation, remote persistence,
   and deployment in completion claims.

## Product memory isolation

- Keep each product's memory and continuity in that product repository. Never
  write a product session into the upstream ATLAS checkout.
- For product work, use `scripts/project_memory.py init|start|close` with the
  explicit product `--project-root`; see `docs/project-local-memory-guide.md`.
- Initialize an unbound product before planning. If legacy state conflicts,
  reconcile it locally while preserving evidence; never fall back to toolkit memory.
- Run start before resuming an initialized product and close after a validated
  checkpoint. Canonical facts belong in its `.claude/memory/`; Obsidian is a
  generated project-local view. Do not copy upstream knowledge during adoption.

## Validation and evidence

- Follow `docs/execution-assurance-guide.md` before executing external skills,
  claiming delivery complete, or admitting primary/fallback models. Use the
  explicit product root; receipts and product sessions never go upstream.
- New execution results default to partial. Completed requires functional
  evidence, exact task criteria and verified remote checkpoint through
  `scripts/execution_assurance.py`; unavailable checks remain pending.
- Discovery trust does not grant execution authority. External code requires
  reviewed full-bundle integrity, scoped tools, sandbox and scan receipts.

- Run the repository validators and `python -m pytest tests -q`.
- Record results with `adapters/codex/instructions/execution-evidence.md`.

## Preferred entry points

- Plan: `adapters/codex/commands/atlas-plan.md`
- Implement: `adapters/codex/commands/atlas-implement.md`
- Review: `adapters/codex/commands/atlas-review.md`
- Release: `adapters/codex/commands/atlas-release.md`
