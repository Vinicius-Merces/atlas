# Database Migration Workflow

## Trigger

A schema, data, ownership, retention, or storage behavior change is required.

## Sequence

1. Define source and destination state.
2. Classify the migration.
3. Identify affected readers and writers.
4. Design compatibility phase.
5. Prepare migration and backfill.
6. Validate on representative data.
7. Deploy in reversible stages.
8. Monitor integrity and performance.
9. Remove transitional paths only after validation.

## Rules

- Prefer expand-and-contract migrations.
- Never assume rollback is possible after destructive writes.
- Define stop conditions before execution.
- Preserve data validation evidence.
