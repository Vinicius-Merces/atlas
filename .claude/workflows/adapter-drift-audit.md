# Adapter Drift Audit Workflow

## Trigger

A supported runtime is prepared for release or canonical assets changed.

## Sequence

1. Compare framework and runtime versions.
2. Compare registry inventories.
3. Validate canonical references.
4. Review generated catalog status.
5. Review support claims.
6. Classify drift.
7. Block release on blocking drift.
8. Record remediation.
