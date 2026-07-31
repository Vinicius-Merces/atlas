# /atlas-test

## Purpose

Create or evaluate a risk-based testing strategy.

## Accepted arguments

- Change scope
- Acceptance criteria
- Architecture
- Existing tests

## Preconditions

- Run from the repository root with `AGENTS.md`, relevant memory, and canonical contracts available.
- Confirm that referenced tasks, files, artifacts, or runtime state exist when the command depends on them.
- Inspect repository status and obtain explicit authorization before any destructive or externally visible action.

## Execution workflow

1. Run test strategy design.
2. Identify critical paths and risk.
3. Select test layers.
4. Define automation and manual checks.
5. Define release exit criteria.

## Output format

- Test matrix
- Automation plan
- Manual validation
- Gaps
- Exit criteria

## Failure behavior

- Stop before mutation when required context, authorization, or a mandatory precondition is missing.
- Do not hide failed gates or claim completion, approval, deployment, or release without supporting evidence.
- Report partial completion, the exact blocker, evidence already collected, pending scope, and the next safe action.
