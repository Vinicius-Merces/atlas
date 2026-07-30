# Migration to 0.1.0-beta.1

## From alpha.14

1. Back up project-specific memory, ADRs, and custom files.
2. Copy the beta package over the repository.
3. Allow matching canonical files to be replaced.
4. Review `compatibility/core-contracts.json`.
5. Review `compatibility/support-policy.md`.
6. Run:
   - `python scripts/validate_registry.py`
   - `python scripts/validate_package.py`
   - `python scripts/validate_contracts.py`
   - `python scripts/run_smoke_tests.py`
7. Review experimental runtime adapter limitations.
8. Commit the migration separately.

## Important

The cumulative package does not delete obsolete files. Review old alpha-specific
or customized files manually.
