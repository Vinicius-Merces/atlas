# Dependency Upgrade Workflow

## Trigger

A dependency should be added, upgraded, replaced, or removed.

## Sequence

1. Identify motivation and urgency.
2. Run dependency impact analysis.
3. Review release notes and advisories.
4. Update dependency in an isolated change.
5. Run targeted and regression validation.
6. Inspect build output and runtime behavior.
7. Update documentation and lockfiles.
8. Confirm rollback.

## Blocking conditions

- Unknown breaking changes
- Unsupported runtime
- Failed mandatory tests
- Critical unresolved security issue
- No rollback for high-impact upgrade
