# Release Artifact Workflow

## Trigger

A versioned ATLAS distribution is prepared.

## Sequence

1. Freeze source version.
2. Validate canonical framework.
3. Build selected runtime adapters.
4. Generate distribution manifest.
5. Generate checksums.
6. Build archive.
7. Validate archive integrity.
8. Store validation evidence.
9. Publish release notes.
10. Approve distribution.

## Blocking conditions

- Version inconsistency
- Missing manifest
- Failed package validation
- Broken adapter
- Corrupted artifact
