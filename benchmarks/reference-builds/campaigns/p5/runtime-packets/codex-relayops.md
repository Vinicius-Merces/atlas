# P5 RelayOps Target Packet - Codex

Execute the canonical `multitenant-subscription-saas` fixture as the isolated Codex target from the exact P5 campaign base commit.

Do not inspect, fetch, diff, cherry-pick, or reuse implementation/evidence/results from any other `bench/p5-relayops-*` branch. Do not search repository history for a RelayOps solution.

Follow `saas-from-brief-delivery` and the existing ATLAS capability set. Route the work through database/schema, authentication, authorization, tenancy/RLS, secrets, mutation design, storage, search, notifications/email, abuse controls, audit/admin, import/export, jobs/cache, payments/webhooks/provider resilience, browser validation, responsive/accessibility/frontend craft, performance, supply-chain, production, and independent review gates. Do not add benchmark-only agents or skills merely to improve the run.

Before implementation:

- record runtime exactly as `codex`;
- record the model string exactly as Codex reports it in this session;
- freeze the P5 run manifest before implementation;
- capture the environment capability manifest using `scripts/capture_benchmark_environment.py`;
- record exact fixture/rubric hashes and the campaign base commit;
- reserve P4 evidence/deployment sidecars and the P5 RelayOps SaaS assurance sidecar.

Before public/browser evidence, freeze a target runner contract matching `benchmarks/reference-builds/campaigns/p5/runner-contract.schema.json` and pass `scripts/validate_benchmark_runner_contract.py`. Its app path, commands, port, health path, and routes are the only target-specific inputs to the shared `.github/workflows/reference-build-controlled-deployment.yml` adapter. Do not create a Codex-only deployment or browser harness.

The implementation must prove more than happy paths. Directly test cross-tenant denial in database/object access, attachment storage, search, cache/job context, notifications/exports, and privileged admin/support actions. Prove explicit tenant context and audit evidence for privileged operations. Prove billing entitlement authority and reconciliation across duplicate, replayed, and out-of-order provider events. Prove role/entitlement revocation does not remain incorrectly available through stale caches. Prove background-job duplicate handling, bounded retry and recovery. Prove provider outage behavior, import row-level partial failure and safe retry, and absence of privileged/provider secrets from browser bundles and client-visible logs.

Browser evidence must cover authentication/organization entry plus a protected operational workflow, customer/work-order mutation, search/filtering, relevant negative/error states, and responsive behavior. If runtime-native browser evidence is unavailable, use the campaign-owned portable browser path and label it `campaign-portable`.

For public HTTPS use the campaign-owned controlled deployment workflow when native hosting would create target-specific infrastructure. Record it truthfully as `controlled-preview`. Controlled preview cannot mark `saas-production-config` as pass; only an enabled campaign-owned claimable-production adapter can satisfy that blocker.

Before scoring, validate the shared P4 evidence assurance, deployment evidence, and the P5 SaaS assurance manifest with `scripts/validate_relayops_assurance.py`. Freeze the first result before any remediation. Independent review must be performed by a reviewer that did not implement the target.
