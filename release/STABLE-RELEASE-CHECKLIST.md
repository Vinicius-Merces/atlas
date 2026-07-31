# ATLAS Stable Release Checklist

Stable promotion is blocked until every item is checked with linked evidence.

- [ ] The release candidate was exercised without blockers.
- [ ] All validators and tests pass on the final source.
- [ ] GitHub-hosted CI is green.
- [ ] Runtime, source-of-truth, catalog, and version drift are zero.
- [ ] SemVer, compatibility, deprecation, and support policies are current.
- [ ] Claude Code and Codex support claims are independently reviewed.
- [ ] Cumulative, incremental, and recovery artifacts are reproducible.
- [ ] Internal manifests and external checksums validate.
- [ ] Clean install, beta.11 upgrade, manual deployment, deletion, and recovery
      simulations pass.
- [ ] Release notes, migration from beta.11, rollback, and known limitations are
      published.
- [ ] The audit bundle passes integrity verification.
- [ ] No unapproved breaking change or policy exception remains.
