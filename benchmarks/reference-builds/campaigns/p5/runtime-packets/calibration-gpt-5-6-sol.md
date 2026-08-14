# P5 RelayOps Calibration Packet - GPT-5.6 Sol

Execute the canonical `multitenant-subscription-saas` fixture as a calibration run from the exact P5 campaign base commit.

Do not inspect, fetch, diff, or reuse implementation/evidence/results from any other `bench/p5-relayops-*` branch. Do not search repository history for a RelayOps implementation.

Follow `saas-from-brief-delivery` and the existing ATLAS responsibilities for database design, authentication, authorization, tenancy/RLS, secret boundaries, forms/mutations, storage, search, notifications, email, abuse controls, audit/admin, import/export, background jobs, caching, payments, webhooks, provider resilience, browser validation, responsive/accessibility/frontend craft, performance, supply chain, release truth, and independent review.

Before implementation:

1. freeze the run manifest;
2. record runtime exactly as `chatgpt` and model exactly as `GPT-5.6 Sol`;
3. capture the environment capability manifest using `scripts/capture_benchmark_environment.py`;
4. reserve paths for the P4 evidence-assurance and deployment sidecars plus the P5 RelayOps SaaS assurance sidecar;
5. record the exact fixture and rubric SHA-256 hashes.

Before public/browser evidence, freeze a target runner contract matching `benchmarks/reference-builds/campaigns/p5/runner-contract.schema.json` and pass `scripts/validate_benchmark_runner_contract.py`. Feed its app path, commands, port, health path, and browser routes into the shared `.github/workflows/reference-build-controlled-deployment.yml` adapter rather than inventing a calibration-only runner.

Positive paths are not sufficient. Directly exercise negative tenant isolation across database/object access, attachment read/write, search, cache/job context, notifications/exports, and privileged admin actions. Exercise duplicate/out-of-order billing webhooks, entitlement reconciliation/revocation, job duplicate/retry/recovery, provider degradation, import partial failure/safe retry, and browser-visible secret scanning.

Use the campaign-owned portable browser and controlled-preview path when native capability is unavailable. `controlled-preview` is real public HTTPS evidence but cannot satisfy `saas-production-config`.

Produce a P5 SaaS assurance manifest matching `benchmarks/reference-builds/campaigns/p5/assurance/relayops-assurance.schema.json` and pass `scripts/validate_relayops_assurance.py` before scoring.

Freeze the first result before remediation. Calibration does not participate in Codex vs Claude target ranking. Independent review must not be self-approval; if an independent reviewer is unavailable, record that truthfully and leave the review unverified.
