# P5 RelayOps Live SaaS Campaign

P5 executes the canonical `multitenant-subscription-saas` fixture as RelayOps under the same clean-room discipline established by P4, but with the P4.1/P4.2/P4.3 environment and evidence normalization applied from the start.

## Purpose

Asteria proved that a benchmark can be distorted when runtime/browser/deployment capability differs between targets. RelayOps therefore starts with one common campaign-owned evidence floor and adds SaaS-specific negative evidence for tenant isolation, billing/entitlements, asynchronous recovery, privileged admin actions, imports/exports, and client secret boundaries.

P5 does **not** add benchmark-only agents or skills. It measures whether the existing ATLAS capability set composes into a credible production SaaS before catalog expansion.

## Clean-room target rules

All target branches start from one frozen campaign base commit.

- `bench/p5-relayops-calibration-gpt-5-6-sol`
- `bench/p5-relayops-codex`
- `bench/p5-relayops-claude-code`

A target must not inspect, fetch, diff, cherry-pick, or reuse implementation/evidence/results from another `bench/p5-relayops-*` branch. Repository history must not be searched for another RelayOps implementation.

The run manifest is frozen before implementation and records the exact fixture/rubric hashes, runtime/model identity, branch/base commit, shared assurance sidecars, SaaS assurance sidecar, and isolation attestation.

## Common environment floor

Compared targets receive the same campaign-owned evidence path where runtime-native capability is unavailable:

- GitHub Actions execution;
- controlled public HTTPS through the P4 deployment adapter;
- portable Chromium browser evidence;
- phone, tablet, laptop, and wide viewports;
- raw evidence preserved separately from attributable target failures;
- controlled preview truth kept separate from claimable production.

Controlled preview can prove public HTTPS/browser behavior, but it cannot satisfy the fixture's `saas-production-config` blocker.

## RelayOps assurance domains

Every frozen run must produce evidence for:

1. authentication/session and organization membership;
2. cross-tenant database denial;
3. cross-tenant storage denial;
4. cross-tenant search denial;
5. tenant-safe cache and background-job context;
6. tenant-safe notification delivery;
7. reconciled billing state and entitlement enforcement;
8. privileged admin/support tenant context plus audit evidence;
9. CSV import partial-failure and retry semantics plus export isolation;
10. absence of privileged/provider secrets from browser-visible surfaces.

Positive-path evidence alone is insufficient for isolation/security checks. Denial behavior must be exercised directly.

## Result truth

The first benchmark result for each target is frozen before remediation. Codex vs Claude comparison is generated only after both first target results are frozen. Calibration never participates in the target ranking.

Independent review must be performed by a reviewer that did not implement the target, with special attention to cross-tenant negative tests, billing divergence/reconciliation, browser reality, and benchmark truthfulness.
