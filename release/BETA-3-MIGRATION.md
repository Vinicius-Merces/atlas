# Migration to 0.1.0-beta.3

## From beta.2

1. Back up project-specific files.
2. Copy the cumulative beta.3 package over the repository.
3. Allow matching canonical files to be replaced.
4. Keep the new root `AGENTS.md`.
5. Run `python scripts/sync_codex_adapter.py`.
6. Run `python scripts/detect_runtime_drift.py`.
7. Run the full validation suite.
8. Commit generated Codex catalogs with the framework update.

## Important

Do not manually fork generated Codex catalogs. Customize runtime behavior in
manual instruction files instead.
