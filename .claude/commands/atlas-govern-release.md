# /atlas-govern-release

## Purpose

Coordinate a formal release go/no-go decision.

## Accepted arguments

- Required: a concise request to coordinate a formal release go/no-go decision.
- Optional: affected paths or artifacts, constraints, risk level, target runtime, and acceptance criteria relevant to this command.

## Preconditions

- Run from the repository root with `AGENTS.md`, relevant memory, and canonical contracts available.
- Confirm that referenced tasks, files, artifacts, or runtime state exist when the command depends on them.
- Inspect repository status and obtain explicit authorization before any destructive or externally visible action.

## Execution workflow

1. Run release governance workflow.
2. Collect gate outcomes.
3. Verify rollout and rollback.
4. Record accepted risks.
5. Return decision and required actions.

## Output format

- A structured `/atlas-govern-release` result containing scope and inputs evaluated.
- Actions, decisions, or findings produced by the command.
- Files or artifacts created, changed, or inspected.
- Validation and review evidence.
- Risks, blockers, and the next safe action.

## Failure behavior

- Stop before mutation when required context, authorization, or a mandatory precondition is missing.
- Do not hide failed gates or claim completion, approval, deployment, or release without supporting evidence.
- Report partial completion, the exact blocker, evidence already collected, pending scope, and the next safe action.
