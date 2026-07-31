# Codex Adoption Guide

## Setup

1. Keep the full ATLAS package in the repository.
2. Use `adapters/codex/README.md` as the Codex entry point.
3. Preserve `.claude/contracts/` and `.claude/memory/` as shared canonical assets.
4. Use Codex command mappings for planning, implementation, review, and release.
5. Run Codex validation before release.

Generated catalogs under `adapters/codex/catalogs/` and JSON maps under
`adapters/codex/generated/` resolve every registered canonical capability.
They are generated artifacts and must not be edited manually.

## Recommended usage

- Planning: `adapters/codex/commands/atlas-plan.md`
- Implementation: `adapters/codex/commands/atlas-implement.md`
- Review: `adapters/codex/commands/atlas-review.md`
- Release: `adapters/codex/commands/atlas-release.md`

## Validation

```bash
python scripts/sync_codex_adapter.py --check
python scripts/validate_codex_adapter.py
python scripts/detect_runtime_drift.py
python scripts/run_codex_tests.py
```

## Customization

Store project-specific instructions separately from the canonical adapter.
Keep durable knowledge under `.claude/memory/`; do not create a Codex-only
memory fork.
