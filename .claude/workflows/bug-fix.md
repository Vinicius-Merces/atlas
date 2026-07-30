# Bug-Fix Workflow

## Trigger

Observed behavior differs from expected behavior.

## Sequence

1. Capture reproduction steps.
2. Identify expected behavior and source of truth.
3. Determine impact and severity.
4. Inspect recent changes and affected contracts.
5. Form a testable root-cause hypothesis.
6. Implement the smallest safe correction.
7. Add or update regression coverage.
8. Validate adjacent behavior.
9. Document the fix when user-visible or architecture-relevant.

## Rules

- Do not patch symptoms when the root cause is known.
- Do not broaden scope without evidence.
- Do not remove validation to make a test pass.
- Report when reproduction is incomplete.
