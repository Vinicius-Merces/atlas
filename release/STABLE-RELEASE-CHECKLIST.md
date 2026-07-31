# ATLAS Stable Release Checklist

Stable promotion is blocked until every item is checked with linked evidence.

- [x] The release candidate was exercised without blockers.
- [x] All validators and tests pass on the final source.
- [x] GitHub-hosted CI is green.
- [x] Runtime, source-of-truth, catalog, and version drift are zero.
- [x] SemVer, compatibility, deprecation, and support policies are current.
- [x] Claude Code and Codex support claims are independently reviewed.
- [x] Cumulative, incremental, and recovery artifacts are reproducible.
- [x] Internal manifests and external checksums validate.
- [x] Clean install, beta.11 upgrade, manual deployment, deletion, and recovery
      simulations pass.
- [x] Release notes, migration from beta.11, rollback, and known limitations are
      published.
- [x] The audit bundle passes integrity verification.
- [x] No unapproved breaking change or policy exception remains.

## Evidence

- `release/0.1.0-VALIDATION.md`
- `release/0.1.0-MIGRATION.md`
- `release/0.1.0-RELEASE-NOTES.md`
- `release/0.1.0.manifest.json`
- `release/evidence/records/rc.1-exercise.json`
- `release/evidence/records/stable-0.1.0-promotion.json`
- `release/evidence/audit-bundle.json`
- Pull request #1 independent support review
- Pull request #3 hosted validation and merge commit
  `5671e55ace0dad2e6e3f1fe3995f4d5e8f595fc8`
