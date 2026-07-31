# ATLAS Codex Runtime

**Support:** Supported compatibility runtime
**Canonical source:** Claude Code implementation and shared ATLAS framework

This adapter provides a functional Codex-oriented representation of ATLAS.
Its generated maps preserve semantic parity; Codex still interprets canonical
workflows, skills, and review gates through the task protocol.

## Structure

- `agents/` role definitions
- `commands/` task entry points
- `skills/` reusable capability mappings
- `workflows/` execution procedures
- `reviews/` verification gates
- `runtime-manifest.json` support and mapping metadata
- `runtime-map.yaml` capability translation
- `catalogs/` generated human-readable capability catalogs
- `generated/*-map.json` machine-readable canonical-to-adapter maps

## Shared canonical assets

Codex uses the same:

- Framework models
- Contracts
- Memory
- ADRs
- Documentation
- Templates
- Blueprints
- Compatibility policies

## Validation

Run:

```bash
python scripts/validate_codex_adapter.py
python scripts/sync_codex_adapter.py --check
python scripts/detect_runtime_drift.py
python scripts/run_codex_tests.py
```

## Limitations

Runtime tool invocation may differ from Claude Code. These differences must not
change semantic responsibility.
