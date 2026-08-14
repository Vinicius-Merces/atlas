# RelayOps Live SaaS Campaign

P5 applies the live reference-build discipline to the canonical RelayOps multi-tenant subscription SaaS fixture without adding benchmark-only agents or skills.

Campaign: `benchmarks/reference-builds/campaigns/p5/campaign.yaml`.
Fixture: `benchmarks/reference-builds/specs/multitenant-subscription-saas.yaml`.

P5 inherits the P4 environment/evidence/deployment assurance and adds a frozen target runner contract plus a SaaS-specific assurance manifest. Codex, Claude Code, and calibration start from the same campaign base commit and must not inspect or reuse another RelayOps target implementation.

The common evidence floor uses the campaign-owned controlled deployment adapter and portable Chromium when runtime-native capability is unavailable. A controlled preview is public HTTPS evidence but is not claimable production and cannot satisfy `saas-production-config`.

Tenant safety is evidence-led: direct cross-tenant denials are required for database/object access, storage, and search, alongside tenant-safe cache/job context, notifications/exports, explicit privileged tenant context, billing reconciliation/revocation, import partial-failure recovery, and zero privileged/provider secrets in browser-visible surfaces.

First results are frozen before remediation. Calibration is excluded from Codex-vs-Claude ranking. Independent review cannot be performed by the implementer.
