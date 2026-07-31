# ATLAS 0.1.0-beta.12 Validation Record

Validation date: 2026-07-30

Runtime: Codex on Windows, with Python dependencies from
`requirements-test.txt`

## Repository gates

- Version, registry, package, contract, schema, documentation, and
  source-of-truth validation: passed
- Codex synchronization, runtime drift, universal contract, and Claude/Codex
  conformance: passed
- Memory freshness and repository/Obsidian knowledge links: passed
- Policy exceptions: zero records; validation passed
- Policy evaluation: 14 passed, 0 warning, 0 approval, 0 blocked
- JSON and YAML parsing: passed
- Python script compilation: passed

## Automated tests

- Smoke: 5 passed
- Contract: 12 passed
- Codex: 16 passed
- Conformance: 26 passed
- Full repository suite: 63 passed

## Distribution validation

- Cumulative archive: integrity validation, deterministic rebuild, and clean
  install simulation passed
- Incremental archive: integrity validation, deterministic rebuild, exact
  beta.11-base preflight, and beta.11-to-beta.12 simulation passed
- Recovery archive: integrity validation, deterministic rebuild, and clean
  recovery simulation passed
- Text payloads are normalized to LF, preventing Windows checkout line endings
  from creating false modifications or cross-platform archive differences
- Incremental deletion simulation removes only explicitly declared files and
  prunes only their empty ancestor directories
- External checksums and internal content manifests detect tampering
- Evidence bundle integrity validation passed for two release records

## Promotion boundary

This record is local execution evidence, not an RC approval. GitHub-hosted CI
must pass on the published branch and an independent reviewer must approve the
candidate before changing the channel to RC.

