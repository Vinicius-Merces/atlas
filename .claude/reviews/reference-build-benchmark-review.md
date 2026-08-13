# Reference Build Benchmark Review

## Review type

Independent end-to-end benchmark evidence and product-readiness review.

## Scope

The exact reference-build fixture, produced repository/commit, deployed environment when required, benchmark submission, scored checks, inherited ATLAS quality gates, and any claim that the run is comparable or production-ready.

## Evidence inspected

Inspect the fixed fixture and rubric version; run metadata; architecture and implementation artifacts; browser evidence; negative security/tenant tests; failure/retry evidence; frontend screenshots/traces; performance/SEO evidence where applicable; deployment/runtime evidence; submission YAML; scorer JSON; and prior independent ATLAS reviews used by the run. Missing evidence must be named.

## Independence

The reviewer must not be the sole implementer of the reference build or the sole author of its evidence. For runtime comparisons, each run may use a separate reviewer, but review criteria must remain equivalent.

## Findings

Record findings against the benchmark axis/check id where possible. Each finding must distinguish observed fact, inference, and unverified claim; cite evidence; explain product/framework impact; and identify whether the root cause is implementation, routing, missing capability, workflow weakness, evidence gap, or fixture ambiguity.

## Severity

Use **Critical**, **High**, **Medium**, **Low**, or **Note**.

Critical or High findings affecting a declared blocking check, tenant/security boundary, authoritative financial state, primary journey, required browser behavior, or benchmark truthfulness prevent approval.

## Required actions

For each unresolved finding, state owner, correction, evidence required to close it, and whether the same fixture must be rerun. A score must never be raised solely because remediation was described; the corrected run/evidence must exist.

## Review areas

### Brief fidelity
- Required users, jobs, content, workflows, and prohibited shortcuts match the fixed fixture.
- No major fixture requirement disappeared behind a technical reinterpretation.

### Architecture and routing
- Architecture fits the product and runtime constraints.
- Capability routing used relevant ATLAS skills/workflows without unnecessary catalog theater.
- Missing behavior is not hidden behind prose or placeholders.

### Implementation completeness
- Required journeys exist end to end.
- Authoritative success state is proved, not inferred from UI.
- Empty, loading, error, conflict, retry, and recovery states exist where the fixture requires them.

### Frontend craft
- Rendered work has product-specific hierarchy and visual authorship.
- Operational products prioritize clarity/density over marketing spectacle.
- Responsive, accessibility, visual regression, and performance evidence exists where required.

### Security and isolation
- Negative authorization/tenant/storage/search/admin tests exist for declared blockers.
- Secrets and privileged providers remain server-side.
- Billing/entitlements and other consequential state are server-authoritative.

### Failure resilience
- Duplicate, retry, stale, provider-outage, queue, webhook, and recovery behavior is proved where applicable.

### Browser and production reality
- Required flows are exercised in a real rendered browser.
- Deployment/domain/configuration evidence is inspected when the fixture requires it.
- Public web claims are based on deployed crawl/index/performance evidence.

### Benchmark integrity
- Every `pass`/`partial` has evidence.
- Blocking checks are not overridden by aggregate score.
- `harness-smoke` is not represented as a live result.
- Runtime comparisons disclose material environment differences.

## Outcome

Return one of: **Approved**, **Approved with conditions**, **Changes required**, or **Blocked**.

`Approved` or `Approved with conditions` does not itself make a result claimable; the deterministic scorer and claim policy make that determination after review evidence is recorded.
