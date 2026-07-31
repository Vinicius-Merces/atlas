# Codex Execution Evidence

## Request

Finish ATLAS according to the finalization brief after the corrected RC passed
hosted validation and was tagged.

## Scope

Promote `0.1.0-rc.1` to stable `0.1.0`, graduate supported runtime and contract
classifications, validate the exact stable tree, and produce reproducible
cumulative, beta.11 incremental, and recovery artifacts.

## Context consulted

- `CODEX-ATLAS-FINALIZATION-BRIEF.md`
- `AGENTS.md`
- `.claude/workflows/release.md`
- `.claude/contracts/review-contract.md`
- `.claude/memory/operations.md`
- Stable and RC release checklists
- Pull requests #1, #2, and #3; tag `v0.1.0-rc.1`

## Roles used

Codex primary agent following release manager, compatibility, policy,
package-integrity, review, and continuity responsibilities. No subagents were
used.

## Files changed

- Controlled version surfaces promoted to `0.1.0`
- Runtime support declarations and compatibility policies promoted to stable
- Core contracts promoted from `stable-rc` to `stable`
- Stable release notes, migration, manifest, validation, checklist, evidence,
  audit bundle, and continuity
- Release-channel tests and validators generalized for stable

## Tests and checks

- Python compilation: passed
- Version, registry, package, contracts, schemas, documentation,
  source-of-truth, Codex synchronization, runtime drift, universal contract,
  conformance, memory, knowledge links, and policy exceptions: passed
- JSON: 113 final files parsed
- YAML: 5 files parsed
- Schemas: 31 schemas and fixtures passed
- Policies: 14 passed, 0 warning, 0 approval, 0 blocked
- Smoke: 5 passed
- Contract: 12 passed
- Codex: 16 passed
- Conformance: 30 passed
- Full suite: 67 passed
- Initial stable artifacts: valid
- Clean install, beta.11 upgrade with 84 explicit legacy-agent deletions, and
  recovery simulation: passed
- Evidence bundle: 7 records passed integrity verification in source,
  cumulative, incremental, and recovery installations
- Incremental operations: 157 additions, 74 replacements, 84 explicit
  deletions
- Cumulative, incremental, and recovery archives: validated and reproduced
  with identical hashes

Final archive SHA-256:

- Cumulative:
  `9160f43a6ea967cd595268204fc3dc71e0ed65c36d6f4b81e168ea1b92cc487d`
- Incremental:
  `840a832e335cfcf5de30bdc69102fd786f1d9cd7fe7047388f372417b8631bde`
- Recovery:
  `28d088d29830f3090ee6bed4397cb754cb7411f2dd895275dbef51f10b8c816c`

## Reviews completed

- RC exercise, compatibility, support, deprecation, rollback, package safety,
  and stable release readiness reviewed
- Independent Claude Code and Codex support review remains inherited from pull
  request #1 because semantic responsibilities are unchanged

## Findings

- Prerelease-only tests and validators required stable-channel generalization
- Runtime support declarations required explicit graduation to `supported`
- Stable artifacts require a direct beta.11 incremental base
- Continuity generators were including ignored `dist/` installation copies;
  source filtering and regression coverage now prevent that contamination

## Assumptions

- Pull request #1 independent review remains applicable to unchanged runtime
  semantic responsibilities

## Remaining risks

- Gemini and Cursor remain experimental

## Documentation and memory updates

- Stable release documentation and evidence added
- Continuity will be refreshed after final validation
