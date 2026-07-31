# ATLAS Support Policy

## Supported runtimes

### Claude Code

Claude Code is the canonical supported runtime. Its `.claude/`
implementation remains the canonical source for runtime behavior.

### Codex

The `adapters/codex/` implementation is a supported compatibility runtime.

Support includes:

- Core role mappings
- Command mappings
- Workflow mappings
- Review mappings
- Generated catalogs and machine-readable maps
- Shared contracts
- Shared memory
- Runtime manifest
- Runtime-specific validation

## Experimental runtimes

### Gemini
### Cursor

Experimental adapters may require manual adjustments.

## Framework compatibility

The stable `0.1.x` line preserves core contract semantics and canonical paths.
Runtime-specific syntax may differ without changing semantic responsibility.

## Stable support window

The current `0.1.x` stable release receives validation, compatibility,
migration, and rollback documentation. Historical prereleases retain migration
documentation but do not receive independent maintenance releases. Upgrade
through documented intermediate patches or use a cumulative package.

## Compatibility boundary

The following are protected across the `0.1.x` stable line unless a
documented migration says otherwise:

- canonical source paths;
- core contract semantics;
- shared memory ownership;
- explicit manual-deployment behavior;
- Claude Code canonical status;
- Codex supported semantic parity.

## Known limitations

- Runtime tool names and invocation differ.
- Codex-specific execution may require explicit orchestration.
- Gemini and Cursor do not receive stable support guarantees.
- Local validation cannot prove that GitHub-hosted CI executed.
- Support is repository-based; no response-time SLA is promised.
