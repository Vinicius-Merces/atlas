# ATLAS Support Policy

## Beta-supported runtimes

### Claude Code

Claude Code is the canonical beta-supported runtime. Its `.claude/`
implementation remains the canonical source for runtime behavior.

### Codex

The `adapters/codex/` implementation is a beta-supported compatibility runtime.

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

The `0.1.0-beta.x` line preserves core contract semantics and canonical paths.
Runtime-specific syntax may differ without changing semantic responsibility.

## Prerelease support window

Before `0.1.0` stable, the current beta or release-candidate line receives full
validation. Historical prereleases retain migration documentation but do not
receive independent maintenance releases. Upgrade through documented
intermediate patches or use a cumulative package.

## Compatibility boundary

The following are protected across the `0.1.0` prerelease line unless a
documented migration says otherwise:

- canonical source paths;
- core contract semantics;
- shared memory ownership;
- explicit manual-deployment behavior;
- Claude Code canonical status;
- Codex beta-supported semantic parity.

## Known limitations

- Runtime tool names and invocation differ.
- Codex-specific execution may require explicit orchestration.
- Gemini and Cursor do not receive beta support guarantees.
- Local validation cannot prove that GitHub-hosted CI executed.
- No stable support SLA applies before `0.1.0`.
