# ATLAS 0.1.0-rc.1 Release Notes

ATLAS `0.1.0-rc.1` promotes the fully validated beta.12 hardening work to the
first release candidate. The RC freezes core contract semantics for stable
validation and introduces no new breaking architecture.

## Included capabilities

- Canonical repository-native agents, contracts, memory, workflows, reviews,
  commands, policies, and evidence
- Beta-supported Claude Code and Codex runtimes with generated parity maps
- Executable version, schema, source-of-truth, runtime, support, CI, package,
  deletion, exception, and cleanliness policies
- Deterministic cumulative, incremental, and recovery packages
- Exact manual deployment operations with visible hidden-directory mapping
- End-to-end lifecycle, continuity, reconciliation, deployment, and
  tamper-detection coverage

## Promotion basis

Pull request #1 finalized beta.12 and was merged to `main` as
`6f8d82dc3241a923ea0ee0f81e1e02e50b45c521`. GitHub-hosted CI and independent
review were reported as passed before merge.

## Stability boundary

Core contract semantics are frozen for the RC line. Stable promotion still
requires the RC to be exercised without blockers and every item in
`release/STABLE-RELEASE-CHECKLIST.md` to be supported by evidence.

