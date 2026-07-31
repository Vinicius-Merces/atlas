# ATLAS Operations Memory

- **Purpose:** Preserve release validation and manual deployment invariants.
- **Scope:** Build, validation, packaging, installation, upgrade, and recovery.
- **Owner:** Release manager
- **Source of truth:** `docs/distribution-guide.md`, `.claude/workflows/release.md`, `release/`, and `policies/`
- **Last reviewed:** 2026-07-30
- **Related contracts or ADRs:** `.claude/contracts/workflow-contract.md`, `.claude/contracts/review-contract.md`

## Release invariants

- `VERSION` is the controlled framework version source.
- Mandatory validators, tests, JSON/YAML parsing, runtime parity, policy
  evaluation, and package validation must pass before release approval.
- Cumulative archives use a versioned root and contain the canonical
  `.claude/` directory.
- Incremental archives map `.claude/` payloads to
  `CLAUDE-DIRECTORY/` and include explicit add, replace, and delete lists.
- Internal content manifests hash archive contents; external checksums hash the
  final closed ZIP.
- Caches, local reports, secrets, `.git/`, and user editor state are excluded
  from release artifacts.

## Rollback

Preserve the installed base version or a validated cumulative recovery
package. Apply only deletions listed by the patch and record manual deployment
results when the update is operationally significant.

## Change triggers

Review this memory when package formats, mandatory gates, support windows,
rollback, or manual deployment behavior changes.
