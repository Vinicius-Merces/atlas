# Runtime Synchronization Policy

## Canonical source

The canonical registry and Claude Code implementation remain the source of truth.

## Codex synchronization

Codex catalogs are generated from the canonical registry and validated before release.

## Blocking drift

The following block a beta release:

- Version mismatch
- Missing registered assets in generated catalogs
- Broken shared contract references
- Missing shared memory references
- Invalid runtime manifest

## Manual guidance

Runtime-specific instructions may remain manually maintained when they describe
tooling or invocation differences rather than canonical capability inventory.
