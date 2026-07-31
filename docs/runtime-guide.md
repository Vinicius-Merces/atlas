# Runtime Guide

## Authority

Claude Code is the canonical runtime. Codex is beta-supported through
`adapters/codex/`. Gemini and Cursor are experimental.

## Shared sources

All supported runtimes use the same:

- `.claude/registry.json`
- `.claude/contracts/`
- `.claude/memory/`
- `framework/`
- `docs/`
- `schemas/`
- `templates/`
- ADRs and compatibility policies

## Runtime translation

Runtime syntax, tool names, and invocation may differ. Semantic
responsibilities, review gates, evidence, source paths, and support claims may
not diverge.

Codex catalogs and maps are generated from the canonical registry. Validate
them with:

```bash
python scripts/sync_codex_adapter.py --check
python scripts/validate_codex_adapter.py
python scripts/detect_runtime_drift.py
python scripts/validate_conformance.py
```

## Continuity

Project briefs, session briefs, resume packets, checkpoints, handoffs, and
evidence live in repository artifacts rather than runtime-specific chat memory.
See [Cross-Session Continuity](cross-session-continuity-guide.md).
