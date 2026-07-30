# ATLAS Support Policy

## Beta-supported

### Claude Code runtime

The `.claude/` implementation is the canonical beta-supported runtime.

Support includes:

- Core agents
- Contracts
- Workflows
- Reviews
- Commands
- Registry
- Runtime metadata
- Package validation
- Smoke and contract tests

## Experimental

### Codex adapter
### Gemini adapter
### Cursor adapter

Experimental adapters provide structural mappings but may require manual
runtime-specific adjustments.

## Framework support

The `0.1.0-beta.x` line preserves core contract semantics and canonical paths
unless a breaking change is explicitly documented with migration guidance.

## Support exclusions

ATLAS does not guarantee compatibility with undocumented project modifications,
unsupported runtime versions, or removed third-party tools.
