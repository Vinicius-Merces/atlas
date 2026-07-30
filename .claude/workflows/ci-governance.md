# CI Governance Workflow

## Trigger

A pull request, release candidate, or protected branch update occurs.

## Sequence

1. Validate repository structure.
2. Validate schemas and metadata.
3. Run policy checks.
4. Run tests and static validation.
5. Validate changed documentation.
6. Validate release metadata when applicable.
7. Publish evidence.
8. Block or approve according to severity.

## Rules

- CI failures must be actionable.
- Warnings must not silently become permanent.
- Exceptions must be explicit and time-bounded.
