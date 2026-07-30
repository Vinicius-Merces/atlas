# ATLAS Support Policy

## Beta-supported runtimes

### Claude Code

The `.claude/` implementation remains the canonical source runtime.

### Codex

The `adapters/codex/` implementation is a beta-supported compatibility runtime.

Support includes:

- Core role mappings
- Command mappings
- Workflow mappings
- Review mappings
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
