# Refactoring Workflow

## Trigger

Internal structure should improve without intentionally changing external
behavior.

## Sequence

1. Define the behavior that must remain unchanged.
2. Identify architecture and contract boundaries.
3. Assess regression risk.
4. Establish or strengthen characterization tests.
5. Refactor in small reversible steps.
6. Run validation after each meaningful step.
7. Review maintainability and performance.
8. Update architecture documentation if boundaries changed.

## Rules

- Do not combine unrelated feature work.
- Do not remove tests to accommodate the refactor.
- Do not claim behavior preservation without evidence.
