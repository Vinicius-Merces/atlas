# /atlas-ai-review

## Purpose

Evaluate an AI-enabled feature for architecture, safety, privacy, quality,
latency, and cost.

## Accepted arguments

- Required: a concise request to evaluate an AI-enabled feature for architecture, safety, privacy, quality, latency, and cost.
- Optional: affected paths or artifacts, constraints, risk level, target runtime, and acceptance criteria relevant to this command.

## Preconditions

- Run from the repository root with `AGENTS.md`, relevant memory, and canonical contracts available.
- Confirm that referenced tasks, files, artifacts, or runtime state exist when the command depends on them.
- Inspect repository status and obtain explicit authorization before any destructive or externally visible action.

## Execution workflow

1. Inspect intended use and architecture.
2. Run AI system review.
3. Inspect evaluation evidence.
4. Review tool permissions and data flow.
5. Report findings and outcome.

## Output format

- A structured `/atlas-ai-review` result containing scope and inputs evaluated.
- Actions, decisions, or findings produced by the command.
- Files or artifacts created, changed, or inspected.
- Validation and review evidence.
- Risks, blockers, and the next safe action.

## Failure behavior

- Stop before mutation when required context, authorization, or a mandatory precondition is missing.
- Do not hide failed gates or claim completion, approval, deployment, or release without supporting evidence.
- Report partial completion, the exact blocker, evidence already collected, pending scope, and the next safe action.
