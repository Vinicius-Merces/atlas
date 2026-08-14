# P5 RelayOps Calibration Baseline

This document records the first frozen GPT-5.6 Sol calibration result for the P5 RelayOps live SaaS campaign. It is diagnostic evidence for campaign readiness, not a Codex or Claude Code target result.

## Identity and freeze points

- Campaign: `p5-live-saas-reference-build-campaign`
- Fixture: `multitenant-subscription-saas`
- Runtime: `chatgpt`
- Model: `GPT-5.6 Sol`
- Frozen P5 campaign base: `99cdbdbf40ca2709bb4e0d99b7d3320d9f89610b`
- Calibration branch: `bench/p5-relayops-calibration-gpt-5-6-sol`
- Pre-implementation run-manifest commit: `c7862936b9f78cba082a80ed15ac5e0fcf506528`
- First implementation + generated evidence freeze: `c601049856d3f7714deb06c1c9f419057acca596`
- First frozen scorer-result commit: `2babc514334b7380335f3c3e7aa93b4b73751d79`
- Fixture SHA-256: `3227ec96f8528476bffbfd860112534158cb5c562a1474e329760685f78d59b9`
- Rubric SHA-256: `6463ae7fde36affecc20eff21f0ec73e04e0fb44c920a3cbc9115502a1b56b31`

The Codex and Claude Code target branches remain untouched at the common P5 base commit. Calibration implementation is not merged into `main` and must not be reused by target runs.

## Official first score

The canonical reference-build scorer produced:

- Score: **79.21 / 100**
- Base outcome: **conditional**
- Final outcome: **blocked**
- Claimable: **false**

Axis scores:

| Axis | Score |
|---|---:|
| Brief Fidelity | 5.83 / 7 |
| Architecture Quality | 11.38 / 13 |
| Capability Routing | 8.00 / 8 |
| Implementation Completeness | 10.40 / 13 |
| Frontend Craft | 6.00 / 8 |
| Security & Isolation | **17.00 / 17** |
| Failure Resilience | 9.60 / 12 |
| Browser Reality | **7.00 / 7** |
| Production Readiness | 4.00 / 10 |
| Independent Review | **0.00 / 5** |

Blocking checks:

1. `saas-auth-org-complete` — partial. Session lifecycle and organization membership work, but account creation/invitation is absent.
2. `saas-billing-entitlement` — partial. Application-authoritative entitlement reconciliation, revocation, duplicate and out-of-order event handling work, but the checkout/provider path is a calibration simulation rather than a real external billing provider.
3. `saas-production-config` — unverified. The public endpoint is a campaign-owned controlled preview, not claimable production.

Independent review is also unverified. The implementing session explicitly did not self-approve an independent review; the recorded outcome is `Changes required`.

## Executed SaaS evidence

The calibration executed fourteen adversarial Node tests successfully after implementation corrections. Evidence covers:

- authenticated session lifecycle and organization membership;
- direct cross-tenant database read/write denial;
- direct cross-tenant attachment read/write denial;
- search isolation with zero foreign-record leakage;
- stale membership/authorization-cache denial;
- tenant-preserving background jobs with idempotency, provider failure, retry and recovery;
- notification recipient isolation;
- billing duplicate-event, out-of-order-event, reconciliation and entitlement-revocation behavior;
- privileged support denial, explicit tenant context and audit evidence;
- CSV row-level partial failure, safe retry and tenant-scoped export;
- browser-visible privileged/provider secret scan with zero exposures;
- HTTP auth, operational, support/admin and security-header behavior.

This direct negative evidence is why all six `security_isolation` checks receive pass status rather than being inferred from source inspection alone.

## Browser reality

A real authenticated Chromium flow passed with zero console errors, page errors, failed requests, HTTP error responses or final horizontal overflow. The flow covered:

- manager sign-in;
- protected Northline dashboard with Harbor data absent;
- customer creation;
- work-order creation and status transition;
- checkout intent without bypassing the reconciled application entitlement;
- visible CSV partial-failure result;
- logout;
- support sign-in with no implicit tenant context;
- explicit Harbor support context;
- Northline customer data absent in Harbor context;
- visible `support.tenant_viewed` audit evidence.

Six authenticated screenshots were frozen. The campaign-portable browser also captured the public controlled-preview path at phone, tablet, laptop and wide viewports. Because those anonymous protected routes redirect to sign-in, authenticated responsive coverage across every viewport remains partial rather than pass.

## Deployment truth

The calibration used the shared P4/P5 controlled deployment path through Cloudflare Quick Tunnel. HTTPS/TLS and public HTTP behavior are real evidence, but the deployment class remains `controlled-preview` and `claimable_production` remains false.

Accordingly, the calibration does not claim:

- a production domain;
- production migration execution;
- production provider configuration;
- production backup/restore validation;
- production latency/resource-budget evidence.

## Environment-capture deviation

The run manifest was correctly frozen before implementation. However, the environment capability sidecar was materialized after implementation had already begun, although its timestamp and notes truthfully record that fact.

The calibration therefore **must not** be cited as proof that environment capability capture occurred before implementation. P5 target packets still require that ordering for the real Codex and Claude Code targets.

## Campaign implication

P5 infrastructure successfully exercised the intended difficult paths: frozen runner contract, exact fixture/rubric hashes, common browser/deployment floor, negative tenant assurance, billing reconciliation, job recovery, admin audit, evidence sidecars and canonical scoring.

The calibration does not provide evidence for adding new agents or skills. Its remaining gaps are implementation completeness, production/provider environment, responsive/accessibility depth, observability/recovery depth and independent review. Target runs should test the existing ATLAS capability set before any catalog expansion is considered.
