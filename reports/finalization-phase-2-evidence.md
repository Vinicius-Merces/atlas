# ATLAS Finalization Phase 2 Evidence

## Request

Continue ATLAS from `0.1.0-beta.11`, validate the repository before editing,
correct known blockers first, and preserve the canonical architecture and
manual deployment flow.

## Scope

Phase 2 blocker remediation only: CI, source-of-truth version, Codex catalogs
and maps, recursive path resolution, support policy, adapter validation, tests,
and execution evidence.

## Context consulted

- `CODEX-ATLAS-FINALIZATION-BRIEF.md`
- `AGENTS.md`
- `VERSION`
- `.claude/registry.json`
- Canonical framework, memory, contracts, workflows, and review gates
- Shared and Codex runtime declarations and manifests
- Compatibility and beta.11 release documents
- `reports/finalization-baseline.md`

## Roles used

- Technical auditor for baseline reproduction
- Runtime synchronization engineer for generated Codex artifacts
- Codex runtime engineer for adapter validation
- Stability engineer for contract and test remediation
- Documentation engineer for support and operating instructions

No independent runtime agent was available in this execution environment.
Automated checks provide independent mechanical evidence; independent human or
separate-agent approval remains a release-governance gate.

## Files changed

- Added a valid GitHub Actions workflow and declared test dependencies.
- Corrected the source-of-truth manifest version.
- Updated support policy and its semantic contract test.
- Strengthened Codex synchronization and validation scripts.
- Generated five machine-readable Codex maps and refreshed all catalogs.
- Updated `AGENTS.md` with missing canonical and evidence references.
- Added the factual baseline report.

## Tests and checks

All commands below exited with code 0 on 2026-07-30:

- `python scripts/validate_registry.py`
- `python scripts/validate_package.py`
- `python scripts/validate_contracts.py`
- `python scripts/validate_codex_adapter.py`
- `python scripts/sync_codex_adapter.py --check`
- `python scripts/detect_runtime_drift.py`
- `python scripts/validate_runtime_contract.py`
- `python scripts/validate_conformance.py`
- `python scripts/validate_source_of_truth.py`
- `python scripts/evaluate_policies.py`
- `python -m compileall -q scripts`
- JSON parse validation: 82 files
- YAML parse validation: 5 files
- `python -m pytest tests -q`: 43 passed

## Reviews completed

- Runtime synchronization review: synchronized
- Codex runtime review: approved for Phase 2 scope
- Source-of-truth review: passed
- Contract compatibility review: passed for changed support assertion

## Findings

- The briefing's malformed CI file was absent in the actual base commit; a new
  workflow was required.
- Canonical agent definitions are split between legacy `agents/` and
  `.claude/agents/`. Generated maps now resolve the real files, but runtime
  consolidation remains required before RC.
- The initial adapter validator did not detect stale generated outputs.
- Test and YAML dependencies were not declared.

## Assumptions

- Python 3.12 is the primary CI runtime; local verification also runs on Python
  3.14.6.
- Existing root-level patch metadata belongs to the cumulative beta history and
  will not be deleted without explicit release analysis.

## Remaining risks

- GitHub Actions syntax is locally parsed as YAML but cannot be claimed green
  until executed by GitHub.
- Version propagation is still manual across several manifests.
- Policy evaluation does not yet enforce all known blocking gates.
- Cumulative and incremental release builders are not yet RC-safe.
- Independent release approval remains outstanding.

## Documentation and memory updates

The durable project architecture did not change in this phase, so canonical
memory was not modified. Operating entry points and the support policy were
updated. Baseline and phase evidence were added under `reports/`.
