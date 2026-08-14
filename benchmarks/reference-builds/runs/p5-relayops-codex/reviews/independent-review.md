# P5 RelayOps Codex — Independent Review

## Outcome

**Changes required.** The frozen first result is correctly `blocked` and non-claimable. The initial review of commit `ba6e40e659756fac2293413d26c4df2e54f39630` found High product/billing/authorization defects. Two remediation passes fixed work-order creation/idempotency, mutation entitlement enforcement, webhook outage replay, ordinary and demo billing role boundaries, technician dashboard/search visibility, and invite password policy. All reproduced code defects passed independent retest and the expanded suite passes 16/16. Approval is still unavailable because the blocking browser-auth flow and production configuration remain unverified, there is no rendered evidence for premium frontend craft, and no separate post-remediation benchmark result has been frozen.

Review type: independent reference-build benchmark, SaaS production-trust, product-completeness, and frontend-craft review.

Scope: the exact P5 Codex target at branch `bench/p5-relayops-codex`, commit `ba6e40e`, followed by a targeted retest of the explicitly supplied uncommitted remediation in `app/src/domain.js`, `app/src/server.js`, and `app/tests/assurance.test.js`; canonical fixture and rubric; P5 target packet and campaign contract; frontend direction; implementation; frozen submission/result; assurance manifests and evidence. No other `bench/p5-relayops-*` branch or RelayOps history was inspected.

## Evidence and checks inspected

- `AGENTS.md`, the ATLAS review contract, benchmark/trust/frontend review gates, and relevant capability memory.
- `benchmarks/reference-builds/specs/multitenant-subscription-saas.yaml` and `scoring-rubric.yaml` in full.
- P5 campaign README, campaign YAML, Codex runtime packet, schemas, run manifest, runner contract, architecture, frontend direction, assurance manifests, local evidence, frozen submission, and frozen scorer result.
- All source, schema, browser JavaScript/CSS, the original 13-test assurance suite, the first remediated 15-test suite, and the final remediated 16-test suite.
- Fixture and rubric hashes matched the run manifest exactly.
- The deterministic scorer reproduced score `75.38`, outcome `blocked`, `claimable: false`, with blocking failures `saas-browser-auth-flow` and `saas-production-config`.
- Initial disposable-copy validation passed 13/13 despite the uncovered gaps. The first remediation passed 15/15; the second remediation passed 16/16 and `node scripts/build.mjs` passed.
- Targeted in-memory/ephemeral HTTP probes first reproduced the product/security defects, then confirmed the final working tree: work-order creation returns 201 and deduplicates; revoked entitlement returns 402 for customer/work-order mutations; webhook outage records pending reconciliation and a healthy duplicate replay reconciles to disabled; technician demo webhook and reconcile both return 403; technician dashboard/search results are assignment-scoped; weak invite password is rejected before invite consumption.
- The Python schema validators could not be rerun in this environment because the required `jsonschema` package is absent. This is a review-runtime limitation, not a validator pass.
- No real browser was available. Source inspection was not treated as rendered, responsive, accessibility, console/network, or visual-quality proof.

## Findings

### F1 — High, resolved in working tree — Primary work-order creation was broken

Affected checks: `saas-work-order-complete`, `saas-required-surfaces`, `saas-operational-goal`, `saas-browser-operational-flow`.

Initial fact: at `ba6e40e`, `RelayOps.createOrder` prepared an `INSERT` with 12 values for 11 named columns and a valid call failed with SQLite error `12 values for 11 columns`.

Retest: the working tree now uses the correct value count, persists the order, event, audit result, and notification, and reuses the same order for a repeated idempotency key. The new test covers creation and deduplication; independent probes confirmed both. The browser journey remains unverified because no real browser is available.

Closure status: implementation defect resolved in the supplied working tree. Still required for benchmark closure: real HTTP/browser journey evidence, invalid-assignee coverage, and a post-remediation scored submission. Preserve the frozen first result.

### F2 — High, resolved for mutations in working tree — Revoked entitlement did not gate operations

Affected checks: blocking `saas-billing-entitlement`, `saas-stale-cache-entitlement`, `saas-operational-goal`.

Initial fact: at `ba6e40e`, `requireEntitlement` had no production caller. After disabling the entitlement, a manager could still persist a customer; the old test called the guard directly rather than a real operation.

Retest: the working tree calls `requireEntitlement` from customer create/update/delete, work-order create/transition, attachment upload, and customer import. The new negative test and independent probe both returned 402 after revocation. This closes the demonstrated mutation bypass. Read-only behavior after revocation should be documented as an explicit product policy rather than inferred.

Closure status: demonstrated mutation defect resolved in the working tree. Still required: document the read-versus-write entitlement matrix and add negative HTTP coverage after cancellation/failed renewal before raising benchmark evidence.

### F3 — High, resolved in working tree — Technician could mutate billing state in the frozen campaign mode

Affected checks: `saas-admin-privilege`, `saas-billing-entitlement`, `saas-routing-trust`.

Initial fact: the frozen runner starts with `RELAYOPS_DEMO_MODE=1`; at `ba6e40e`, both demo webhook and reconcile accepted a technician and could mutate/reconcile entitlement.

Retest: the final working tree routes demo events through `demoWebhook(ctx, input)` and reconciliation through `reconcileFor(ctx)`, both enforcing manager/billing role at the domain boundary. The final suite exercises the real HTTP endpoints; independent output shows technician demo webhook 403 and reconcile 403. Allowed demo events are audited.

Closure status: reproduced privilege escalation resolved in the working tree. Provider-origin webhook authentication remains separately governed by HMAC and is not a user-role endpoint.

### F4 — High, resolved in working tree — Accepted webhook could not recover from reconciliation outage

Affected checks: `saas-distributed-state`, `saas-webhook-replay`, `saas-provider-outage`, `saas-billing-entitlement`, `saas-recovery`.

Initial fact: at `ba6e40e`, an outage after durable event acceptance caused duplicate replay to return early, leaving provider cancellation divergent from active application entitlement.

Retest: the working tree records `reconciliationPending` when reconciliation returns 503. Replaying the accepted event after recovery calls reconciliation and returns `reconciled: true`; independent probes confirmed final entitlement disabled. The new test covers this exact failure sequence.

Closure status: reproduced defect resolved in the working tree. Residual production risk remains because retry is caller-driven replay rather than a demonstrated durable scheduler, and no provider-backed/browser evidence exists.

### F5 — High, resolved in working tree — Technician dashboard violated the established assignment boundary

Affected checks: `saas-personas-workflows`, `saas-auth-org-complete`, `saas-admin-privilege`.

Initial fact: `listOrders` and `order` enforced technician assignment, but the default dashboard returned the entire tenant queue; a technician probe received an unassigned order.

Retest: the final working tree applies assignment predicates to technician dashboard counts/queue and to technician customer/work-order search. The new test requires every returned work order to be assigned to the technician, and independent probes no longer reproduce unassigned dashboard exposure.

Closure status: reproduced dashboard/search visibility defect resolved in the working tree. A real browser role journey remains required by the fixture.

### F6 — High — Frozen benchmark statuses overstate proved completeness and resilience

Affected checks: benchmark truthfulness, especially `saas-work-order-complete`, `saas-billing-entitlement`, `saas-distributed-state`, `saas-webhook-replay`, `saas-provider-outage`, and `saas-stale-cache-entitlement`.

Observed fact: the frozen first submission marks all of those checks `pass`, commonly citing the aggregate assurance JSON. At the frozen commit, that evidence did not exercise broken order creation, effective entitlement enforcement, unauthorized billing endpoints, or reconciliation-outage replay. The final working-tree remediation and 16-test suite now cover those gaps, technician assignment visibility, invite policy, HTTP work-order creation, and direct billing-role denial. The frozen first artifact must remain historical. Its overall `blocked`/non-claimable result and browser/production `unverified` statuses are truthful.

Impact: the reported first-result axis score (`implementation_completeness` 13/13 and `failure_resilience` 12/12) was not a faithful representation of its commit. The remediation improves current evidence but does not retroactively change that frozen result and is not yet represented by a new scored submission.

Required correction: preserve the historical first artifact and create a separate post-remediation submission/result with explicit 16-test and independent-retest evidence. Historical artifacts must not be silently rewritten; comparisons must disclose this review and distinguish first-result from remediated-result scores.

### F7 — Medium — Premium frontend craft remains unverified

Affected checks: `saas-information-density`, `saas-responsive`, `saas-accessibility`, `saas-visual-authorship`, all `browser_reality` checks, and `saas-performance`.

Observed fact: the exact commit contains no screenshots, viewport captures, browser trace, keyboard/focus audit, contrast samples, overflow results, console/network capture, visual-regression output, or authenticated performance evidence. The evidence-assurance manifest explicitly records browser and visual regression as unavailable. Therefore this review cannot determine that the shipped UI is rendered correctly or reaches premium craft.

Source-only assessment: the “calm field-service control room” thesis, Relay Line vocabulary, petrol/orange state grammar, tabular operational tables, explicit empty/error/success states, reduced-motion CSS, and off-canvas/table-overflow intent are authored and product-specific. They are promising implementation patterns, not rendered proof. The CSS also contains a large appended “premium control-room layer” overriding an earlier system, so cascade behavior and intermediate-width composition particularly require real inspection.

Required correction: collect campaign-portable real-browser evidence for every acceptance-matrix route/state at 360/768/1280/1920, including keyboard/focus, accessible names, dialog behavior, contrast, overflow, reduced motion, errors, console/network, and representative performance. Obtain an independent rendered craft review before raising frontend statuses.

### F8 — Medium — Mandatory campaign sidecar/validation evidence is incomplete

Affected checks: campaign completion, `saas-production-config`, benchmark evidence integrity.

Observed fact: at exact commit `ba6e40e`, `run-manifest.json` points to `assurance/deployment-evidence.json`, but that file is absent. No controlled preview or claimable-production evidence exists. The frozen result correctly leaves production config unverified, but the packet's pre-scoring sidecar validation sequence is not reproducible from the commit. Local validator rerun was additionally blocked by missing `jsonschema` in this review runtime.

Required correction: keep production config non-pass; provide the campaign-owned deployment sidecar when the shared workflow runs, preserve raw validation output, and rerun the specified validators in a provisioned environment.

### F9 — Medium, resolved in working tree — Invitation acceptance bypassed password policy

Affected checks: `saas-auth-org-complete`, authentication/session trust.

Initial fact: registration enforced a 10-character password, but invite acceptance hashed any string for a new user, including an empty password.

Retest: the final working tree validates new invitee name and 10-character minimum before entering the transaction or consuming the invite. The new test proves weak-password rejection, successful strong-password acceptance, and single-use replay denial.

Closure status: reproduced password-policy bypass resolved in the working tree. The test also proves successful login after acceptance; expiry, email binding, and the rendered invite journey remain without real-browser evidence.

## Strong patterns worth preserving

- Tenant predicates are placed inside customer, work-order, attachment, search, notification, export, cache, and job queries rather than applied after global reads.
- The cross-tenant suite uses two real tenant fixtures and positive controls before denial assertions for database/object, storage, and search. This is materially stronger than happy-path-only evidence.
- Sessions are opaque/HttpOnly, membership and authorization version are reloaded from authoritative state, origin checks protect mutations, and logs redact sensitive key classes.
- Support inspection requires global support role, explicit tenant context, reason, and an allowed audit record; ordinary manager escalation is denied.
- Composite tenant keys, attachment reauthorization, import source/idempotency records, job effect uniqueness, webhook signatures/order checks, and cache versioning are sound foundations; the reproduced local failure paths are now covered by regression tests.
- The remediation responded directly to executable counterexamples: it added work-order idempotency, placed entitlement checks on consequential mutations, made accepted-event replay resume reconciliation, and moved ordinary reconciliation behind a role-aware domain method. These are strong corrective patterns worth retaining.
- Benchmark truth is appropriately conservative for browser, deployment, RLS, live providers, and claimability; the frozen result does not pretend local source inspection is production or browser evidence.
- The frontend direction is unusually specific to field-service operations and avoids a generic marketing dashboard thesis. Preserve the Relay Line, exception-first color use, operational density, and restrained product vocabulary during remediation.

## Required changes before approval

1. Product/QA owner: retain the 16-test remediation coverage and prove the complete auth/invite, work-order create/transition/attachment/event/audit, search/filter, error, and role-denial journeys in a campaign-portable real browser.
2. Benchmark owner: preserve `result-first.json`, publish a separate post-remediation submission/result with the new assurance evidence, and keep the run non-claimable while blockers remain.
3. Frontend/QA owner: obtain the required rendered responsive, accessibility, visual-regression, console/network, and performance evidence; then perform an independent premium craft review.
4. Campaign owner: produce/validate the missing deployment sidecar through the shared adapter; only a claimable-production deployment may pass `saas-production-config`.
5. Evidence owner: rerun the runner, evidence-assurance, RelayOps assurance, deployment, and benchmark-pack validators in an environment containing `jsonschema`, and preserve raw output.

All reproduced implementation defects in F1-F5 and F9 are independently retest-green in the final working tree. The historical benchmark-truth finding in F6, missing post-remediation score, and mandatory browser/production evidence blockers still prevent approval. Governance prose or source inspection alone cannot close them.

## Residual risks

- SQLite application scoping is not PostgreSQL RLS and does not prove multi-instance production isolation, migration safety, backup automation, or concurrency behavior.
- Provider implementations are deterministic sandbox equivalents; no live payment/email contract, credential separation, rate-limit behavior, or provider observability is proved.
- Real browser behavior, responsive composition, accessibility, visual polish, console/network health, and performance remain unknown.
- Public HTTPS, persistent secrets/configuration, domain ownership, production migrations, recovery drills, and SLA are unproved; `saas-production-config` remains a blocker.
- The local assurance suite writes its evidence output during execution, so independent raw command output and immutable provenance remain important when the campaign evidence is finalized.
