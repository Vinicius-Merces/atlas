# ATLAS 0.1.0-rc.1 Validation Record

Validation date: 2026-07-30

Promotion base: `0.1.0-beta.12` at merge commit
`6f8d82dc3241a923ea0ee0f81e1e02e50b45c521`

## External promotion evidence

- Pull request #1 merged the finalized beta.12 source into `main`
- GitHub-hosted CI was reported as passed before merge
- Independent review was reported as passed before merge
- The remote PR head and merge refs were verified through Git

## Repository gates

- Version, registry, package, contracts, schemas, documentation, and
  source-of-truth: passed
- Codex synchronization, runtime drift, universal contract, and Claude/Codex
  conformance: passed
- Memory freshness and repository/Obsidian knowledge links: passed
- Policy exceptions: zero; validation passed
- Policy evaluation: 14 passed, 0 warning, 0 approval, 0 blocked
- JSON: 110 files parsed
- YAML: 5 files parsed
- Schemas: 31 schemas and fixtures passed
- Python script compilation: passed

## Automated tests

- Smoke: 5 passed
- Contract: 12 passed
- Codex: 16 passed
- Conformance: 26 passed
- Full repository suite: 63 passed

## Distribution gates

- Cumulative, incremental, and recovery archives validated
- All archives rebuilt with identical SHA-256 hashes
- Clean cumulative and recovery installations passed
- Exact beta.12-to-RC incremental preflight and simulation passed
- Manual operations and hidden-directory mappings matched the patch manifest
- Audit evidence passed integrity validation in source and installed packages

## Stable boundary

This validation approves the first release candidate, not `0.1.0` stable.
Stable remains blocked until the RC is exercised without blockers and
`release/STABLE-RELEASE-CHECKLIST.md` is complete.
