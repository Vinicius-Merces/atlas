# Runtime Synchronization Workflow

## Trigger

Canonical registry collections or supported runtime mappings change.

## Sequence

1. Validate canonical registry.
2. Generate runtime catalogs.
3. Compare generated and committed output.
4. Update runtime manifest.
5. Run adapter validation.
6. Run drift detection.
7. Run runtime tests.
8. Publish synchronization report.
