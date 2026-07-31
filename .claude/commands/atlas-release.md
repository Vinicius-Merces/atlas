# /atlas-release

## Purpose

Evaluate release readiness and prepare a release package.

## Accepted arguments

- Required: a concise request to evaluate release readiness and prepare a release package.
- Optional: affected paths or artifacts, constraints, risk level, target runtime, and acceptance criteria relevant to this command.

## Preconditions

- Run from the repository root with `AGENTS.md`, relevant memory, and canonical contracts available.
- Confirm that referenced tasks, files, artifacts, or runtime state exist when the command depends on them.
- Inspect repository status and obtain explicit authorization before any destructive or externally visible action.

## Execution workflow

1. Run the release workflow.
2. Confirm version and changelog.
3. Validate mandatory gates.
4. Inspect migrations and rollback.
5. Prepare release notes.
6. Return approval or blocking findings.

## Output format

- Release version
- Included changes
- Validation summary
- Known risks
- Rollback plan
- Release outcome

## Failure behavior

- Stop before mutation when required context, authorization, or a mandatory precondition is missing.
- Do not hide failed gates or claim completion, approval, deployment, or release without supporting evidence.
- Report partial completion, the exact blocker, evidence already collected, pending scope, and the next safe action.
