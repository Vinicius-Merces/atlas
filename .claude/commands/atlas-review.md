# /atlas-review

## Purpose

Run the review gates relevant to a proposed or completed change.

## Accepted arguments

- Required: a concise request to run the review gates relevant to a proposed or completed change.
- Optional: affected paths or artifacts, constraints, risk level, target runtime, and acceptance criteria relevant to this command.

## Preconditions

- Run from the repository root with `AGENTS.md`, relevant memory, and canonical contracts available.
- Confirm that referenced tasks, files, artifacts, or runtime state exist when the command depends on them.
- Inspect repository status and obtain explicit authorization before any destructive or externally visible action.

## Execution workflow

1. Classify change impact.
2. Select architecture, security, UX, QA, and documentation reviews.
3. Inspect available evidence.
4. Record findings and severity.
5. Return an approval outcome.

## Output format

- Reviews performed
- Findings
- Validation gaps
- Required actions
- Final outcome

## Failure behavior

- Stop before mutation when required context, authorization, or a mandatory precondition is missing.
- Do not hide failed gates or claim completion, approval, deployment, or release without supporting evidence.
- Report partial completion, the exact blocker, evidence already collected, pending scope, and the next safe action.
