# Contract Testing Workflow

## Trigger

Stable contracts, registry structure, canonical paths, or runtime metadata
change.

## Sequence

1. Read stable contract manifest.
2. Identify affected contract tests.
3. Add or update positive cases.
4. Add or update negative cases.
5. Run contract suite.
6. Validate failure diagnostics.
7. Record coverage gaps.
8. Publish evidence.
