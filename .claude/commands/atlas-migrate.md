# /atlas-migrate

## Purpose

Plan and govern a schema, data, or infrastructure migration.

## Accepted arguments

- Current state
- Target state
- Constraints
- Availability requirements

## Preconditions

- Run from the repository root with `AGENTS.md`, relevant memory, and canonical contracts available.
- Confirm that referenced tasks, files, artifacts, or runtime state exist when the command depends on them.
- Inspect repository status and obtain explicit authorization before any destructive or externally visible action.

## Execution workflow

1. Classify migration risk.
2. Run relevant migration analysis skill.
3. Define compatibility phases.
4. Define validation and stop conditions.
5. Define rollback or forward-fix.
6. Produce execution plan.

## Output format

- Migration class
- Phases
- Risks
- Validation
- Stop conditions
- Recovery strategy

## Failure behavior

- Stop before mutation when required context, authorization, or a mandatory precondition is missing.
- Do not hide failed gates or claim completion, approval, deployment, or release without supporting evidence.
- Report partial completion, the exact blocker, evidence already collected, pending scope, and the next safe action.
