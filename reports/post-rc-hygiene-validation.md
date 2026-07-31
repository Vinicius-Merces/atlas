# Codex Execution Evidence

## Request

Continue ATLAS after the RC promotion merge and finish all work that can be
completed without inventing release evidence.

## Scope

Reconcile the repository with the merged RC state, remove accidentally tracked
user-local editor state, and add a policy regression gate.

## Context consulted

- `CODEX-ATLAS-FINALIZATION-BRIEF.md`
- `AGENTS.md`
- `.claude/memory/operations.md`
- `.claude/workflows/release.md`
- `adapters/codex/commands/atlas-release.md`
- `adapters/codex/instructions/execution-evidence.md`
- Pull request #2 Git refs and merge commit

## Roles used

Codex primary agent following release management, policy, package-integrity,
and continuity responsibilities. No subagents were used.

## Files changed

- `.gitignore`
- `.vscode/extensions.json` removed from Git tracking and preserved locally
- `policies/repository_cleanliness.json`
- `scripts/evaluate_policies.py`
- `tests/conformance/test_repository_cleanliness.py`
- RC validation and continuity records

## Tests and checks

- Repository cleanliness regression tests: 2 passed
- Full repository suite: 65 passed
- Tracked JSON: 108 files parsed
- Tracked YAML: 5 files parsed
- Registry, package, contracts, schemas, Codex synchronization, runtime,
  conformance, source-of-truth, memory, links, documentation, and policy
  validators: passed
- Policy evaluation: 14 passed, 0 warning, 0 approval, 0 blocked
- Python script compilation: passed
- Cumulative, incremental, and recovery archives: valid and reproduced with
  identical hashes
- Clean RC installation, beta.12 incremental upgrade, and recovery
  installation: passed
- Evidence integrity in all three installed modes: 4 records passed

Final archive SHA-256:

- Cumulative:
  `ca85cd7d9e82e3e8faacf0a900fb29f631cdeadf2b02a84e1180f4ee0d11fa64`
- Incremental:
  `3c3bfc4f9b9c0ba80a9d3a19d6b81f87db6115fd6cf53d38c2cf456e96a6d31c`
- Recovery:
  `45bf9f79a2b3253ff6f1a8b244b66992be8250432356c208bc99b005fc6ee222`

## Reviews completed

- Verified pull request #2 merge commit
  `0c7208a302d536f0ff00c949d5a6bdaa6c6c5a03`
- Reviewed package exclusion behavior for `.vscode`
- Reviewed synthetic clean and violating repository cases

## Findings

- Pull request #2 accidentally reintroduced `.vscode/extensions.json` into Git
  even though release packaging already excluded `.vscode`
- Repository cleanliness policy did not explicitly reject that user-local file
- The RC promotion evidence still lacked the pull request #2 merge reference

## Assumptions

- `.vscode/extensions.json` is user-local editor state and must remain available
  on the workstation while being absent from Git and release artifacts

## Remaining risks

- GitHub-hosted checks for this corrective branch must pass before merge
- Stable promotion remains blocked until the RC exercise and stable checklist
  have truthful, reviewable evidence
- Gemini and Cursor remain experimental

## Documentation and memory updates

- RC checklist, validation, manifest, and continuity records are reconciled
  with pull request #2
- The next session can resume from the post-RC corrective branch without
  relying on chat history
