# Runtime Synchronization Guide

## Canonical first

Change canonical ATLAS assets before changing generated runtime catalogs.

## Generate

Run:

```bash
python scripts/sync_codex_adapter.py
```

## Verify

Run:

```bash
python scripts/sync_codex_adapter.py --check
python scripts/detect_runtime_drift.py
```

## Manual files

Codex task protocols, execution evidence, and tool-specific instructions may be
maintained manually.

## Generated files

Catalogs and generated indexes should never be edited directly.
