# /atlas-plan

## Purpose

Generate a governed implementation plan before code changes.

## Accepted arguments

- User request
- Relevant files or systems
- Constraints

## Preconditions

- Run from the repository root with `AGENTS.md`, relevant memory, and canonical contracts available.
- Confirm that referenced tasks, files, artifacts, or runtime state exist when the command depends on them.
- Inspect repository status and obtain explicit authorization before any destructive or externally visible action.

## Execution workflow

1. Resolve context and memory.
2. Classify scope and risk.
3. Identify responsible agents.
4. Compare solution options.
5. Define execution sequence.
6. Define validation and rollback.
7. Produce acceptance criteria.

## Output format

- Scope
- Assumptions
- Plan
- Agents
- Risks
- Validation
- Acceptance criteria

## Failure behavior

- Stop before mutation when required context, authorization, or a mandatory precondition is missing.
- Do not hide failed gates or claim completion, approval, deployment, or release without supporting evidence.
- Report partial completion, the exact blocker, evidence already collected, pending scope, and the next safe action.
