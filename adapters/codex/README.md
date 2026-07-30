# ATLAS Codex Runtime

**Support:** Beta-supported compatibility runtime  
**Canonical source:** Claude Code implementation and shared ATLAS framework

This adapter provides a functional Codex-oriented representation of ATLAS.

## Structure

- `agents/` role definitions
- `commands/` task entry points
- `skills/` reusable capability mappings
- `workflows/` execution procedures
- `reviews/` verification gates
- `runtime-manifest.json` support and mapping metadata
- `runtime-map.yaml` capability translation

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
python scripts/run_codex_tests.py
```

## Limitations

Runtime tool invocation may differ from Claude Code. These differences must not
change semantic responsibility.
