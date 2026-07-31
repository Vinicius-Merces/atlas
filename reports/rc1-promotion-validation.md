# Codex Execution Evidence

## Request

Continue ATLAS after pull request #1 passed hosted CI and independent review
and was merged.

## Scope

Promote merged `0.1.0-beta.12` source to `0.1.0-rc.1`, validate the exact RC
tree, and prepare reproducible cumulative, incremental, and recovery artifacts.

## Context consulted

- `AGENTS.md`
- `.claude/workflows/release.md`
- `.claude/memory/operations.md`
- `adapters/codex/commands/atlas-release.md`
- `release/RC-RELEASE-CHECKLIST.md`
- `release/STABLE-RELEASE-CHECKLIST.md`
- Pull request #1 Git refs and merge commit

## Roles used

Codex primary agent following release manager, compatibility, package
integrity, policy, evidence, and continuity responsibilities. No subagents
were used. Pull request #1 supplied the independent external review gate.

## Files changed

- Controlled version surfaces promoted to `0.1.0-rc.1`
- Changelog, README, release manifest, RC notes, migration, checklist,
  validation, evidence, audit bundle, and continuity
- Contract stability schema and manifest promoted to `rc` / `stable-rc`
- Semantic-version matrix and known limitations corrected
- Version-history and prerelease tests generalized for RC

## Tests and checks

- Python compilation: passed
- Version, registry, package, contracts, schemas, Codex synchronization,
  runtime drift, runtime contract, conformance, source of truth, memory,
  knowledge links, documentation, and policy exceptions: passed
- JSON: 110 files parsed
- YAML: 5 files parsed
- Schemas: 31 schemas and fixtures passed
- Policies: 14 passed, 0 warning, 0 approval, 0 blocked
- Smoke: 5 passed
- Contract: 12 passed
- Codex: 16 passed
- Conformance: 28 passed
- Full suite: 65 passed
- Evidence bundle: 4 records passed integrity verification
- Incremental operations: 7 additions, 40 replacements, 0 deletions
- Cumulative, incremental, and recovery archives: validated, reproducible, and
  installed successfully

Final archive SHA-256:

- Cumulative:
  `ca85cd7d9e82e3e8faacf0a900fb29f631cdeadf2b02a84e1180f4ee0d11fa64`
- Incremental:
  `3c3bfc4f9b9c0ba80a9d3a19d6b81f87db6115fd6cf53d38c2cf456e96a6d31c`
- Recovery:
  `45bf9f79a2b3253ff6f1a8b244b66992be8250432356c208bc99b005fc6ee222`

## Reviews completed

- Pull request #1 hosted CI and independent review were reported as passed
- Merge commit `6f8d82dc3241a923ea0ee0f81e1e02e50b45c521` and PR refs verified
- Local compatibility, contract, package-integrity, policy, deletion-safety,
  migration, rollback, and release review completed

## Findings

- Two contract tests encoded beta-only assumptions and were generalized to
  supported prerelease channels
- The contract stability schema lacked an `rc` state
- Known limitations incorrectly described Codex as experimental and understated
  local link validation
- The RC incremental migration requires only additions and replacements

## Assumptions

- The repository owner's statement accurately represents the private GitHub CI
  and review state for pull request #1
- The merged main commit is the immutable beta.12 incremental base

## Remaining risks

- The exact RC promotion branch still requires hosted CI and review before
  merge
- Stable promotion requires real-project RC exercise evidence
- Gemini and Cursor remain experimental

## Documentation and memory updates

- RC release notes, migration, validation, manifest, checklist, support,
  compatibility, rollback, limitations, evidence, and audit records updated
- Continuity project/session briefs, resume packet, drift report, and
  reconciliation proposal refreshed for `0.1.0-rc.1`
