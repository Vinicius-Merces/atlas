# ATLAS Capability Registry

This directory contains the compact discovery surface for ATLAS capabilities.

- `capabilities.json` is the complete generated machine-readable catalog.
- `ard-index.json` is the compact index intended for bounded discovery.
- `trust-policy.json` defines provenance and admission defaults.

Generate or verify the artifacts with:

```bash
python scripts/generate_capability_fabric.py
python scripts/generate_capability_fabric.py --check
python scripts/discover_capabilities.py "browser security review"
```

Do not edit generated files manually. Canonical definitions remain under
`.claude/` and are registered in `.claude/registry.json`.
