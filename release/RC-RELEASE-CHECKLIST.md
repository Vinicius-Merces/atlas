# ATLAS Release Candidate Checklist

- [x] All repository validators pass.
- [x] All tests pass.
- [x] CI YAML is valid and GitHub-hosted CI status is recorded.
- [x] JSON, YAML, and schemas validate.
- [x] Version, registry, source-of-truth, Codex, and runtime drift checks pass.
- [x] Memory freshness, continuity, and Obsidian links pass.
- [x] Policy evaluation has no blocking result.
- [x] Cumulative, incremental, and recovery packages validate.
- [x] Clean install and beta.12 upgrade simulations pass.
- [x] Manual deployment and deletion handling pass.
- [x] Release notes, migration, support, compatibility, rollback, and known
      limitations are complete.
- [x] Audit evidence and remaining runtime limitations are recorded.

## Evidence

- `release/RC-1-VALIDATION.md`
- `release/evidence/records/rc.1-promotion.json`
- `release/evidence/records/manual-deployment-rc.1.json`
- `release/evidence/audit-bundle.json`
- Pull request #1 and merge commit
  `6f8d82dc3241a923ea0ee0f81e1e02e50b45c521`
- Pull request #2 and RC merge commit
  `0c7208a302d536f0ff00c949d5a6bdaa6c6c5a03`

GitHub-hosted CI and independent review for the finalized beta.12 source were
reported as passed before pull request #1 merged. The RC promotion delta is
limited to version, maturity, compatibility, release, evidence, and test
generalization changes, was merged by pull request #2, and is revalidated
locally in full.
