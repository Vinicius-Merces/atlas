# ATLAS Finalization Baseline

## Audit metadata

- Audit date: 2026-07-30
- Framework version: `0.1.0-beta.11`
- Base branch: `main`
- Finalization branch: `finalization/0.1.0-rc.1`
- Base commit: `7393c2962a98c0dbd13c328bd27ef8a7fd4d0bd1`
- Operating system: Microsoft Windows 10.0.19045 x64
- PowerShell: 5.1.19041.6456
- Python: 3.14.6

## Protected initial state

The initial worktree contained one pre-existing, untracked user path:

```text
?? .vscode/extensions.json
```

It was not modified. The canonical `.claude/registry.json` exists. A permanent
repository-level `CLAUDE-DIRECTORY/` does not exist. `.gitignore` and
`.github/workflows/validate.yml` do not exist in the base commit.

The mandatory audit generated the following local artifacts after the initial
status was captured:

- `.atlas/policy/policy-report.json`
- Python `__pycache__` files
- pytest cache files

These are execution artifacts, not part of the protected initial user state.

## Mandatory command results

| Command | Exit code | Result |
|---|---:|---|
| `python --version` | 0 | `Python 3.14.6` |
| `git status --short` | 0 | `?? .vscode/` |
| read `VERSION` | 0 | `0.1.0-beta.11` |
| `python scripts/validate_registry.py` | 0 | Registry valid |
| `python scripts/validate_package.py` | 0 | 879 files inspected; passed |
| `python scripts/validate_contracts.py` | 0 | 6 contracts and 10 canonical paths valid |
| `python scripts/validate_codex_adapter.py` | 0 | Passed, despite stale generated catalogs |
| `python scripts/sync_codex_adapter.py --check` | 1 | Seven Codex generated artifacts stale |
| `python scripts/detect_runtime_drift.py` | 1 | Drift caused by stale Codex artifacts |
| `python scripts/validate_runtime_contract.py` | 0 | Passed |
| `python scripts/validate_conformance.py` | 0 | Claude Code and Codex declarations conform |
| `python scripts/validate_source_of_truth.py` | 1 | Manifest version mismatch |
| `python scripts/evaluate_policies.py` | 0 | Report generated; known blockers were not enforced |
| `python -m compileall -q scripts` | 0 | Passed |
| `python -m pytest tests -q` (initial) | 1 | `pytest` was not installed |
| JSON parse validation | 0 | 77 JSON files parsed |
| YAML parse validation | 0 | 4 YAML files parsed with PyYAML 6.0.3 |
| `python -m pytest tests -q` (after environment setup) | 1 | 39 passed, 4 failed |

The audit environment initially lacked both `pytest` and PyYAML. They were
installed into the current user's Python environment to complete the baseline;
the repository still has no declared test dependency file at this point.

## Reproduced failures

### Codex catalog synchronization

`sync_codex_adapter.py --check` reported these stale files:

```text
adapters/codex/catalogs/agents.md
adapters/codex/catalogs/commands.md
adapters/codex/catalogs/skills.md
adapters/codex/catalogs/workflows.md
adapters/codex/catalogs/reviews.md
adapters/codex/generated/INDEX.md
adapters/codex/generated/catalog-manifest.json
```

The generated agent count is 64 while the registry contains 86 agents.
`detect_runtime_drift.py` fails as a consequence.

### Source-of-truth version drift

`adapters/shared/source-of-truth-manifest.json` declares
`0.1.0-beta.9`, while `VERSION` declares `0.1.0-beta.11`.

### Support policy contract

`compatibility/support-policy.md` identifies Claude Code as canonical but does
not include the contract-test phrase `canonical beta-supported runtime`.

### Test suite

After installing the missing test runner, pytest reported:

```text
4 failed, 39 passed
```

The failing tests were:

1. `tests/codex/test_full_registry_parity.py::test_every_registered_item_appears_in_codex_catalog`
2. `tests/codex/test_generated_catalogs.py::test_generated_collection_counts_match_registry`
3. `tests/conformance/test_memory_governance.py::test_source_of_truth_manifest_matches_version`
4. `tests/contract/test_support_policy.py::test_support_policy_declares_canonical_runtime`

### CI and policy coverage

The briefing described malformed CI YAML, but the repository has no `.github/`
directory at the base commit. CI therefore cannot run until a workflow is
created. Policy evaluation exits successfully despite catalog drift,
source-of-truth drift, the support-policy failure, and absent CI.

## Baseline conclusion

The repository is a partially applied `0.1.0-beta.11` state. Its registry,
contracts, package structure, runtime declarations, JSON, and existing YAML are
valid, but it is not release-candidate ready. The known blocker set is confirmed
and expanded by missing CI and undeclared test dependencies. No promotion is
permitted until the mandatory validators, test suite, runtime parity, release
engineering, documentation, and manual-deployment gates pass.
