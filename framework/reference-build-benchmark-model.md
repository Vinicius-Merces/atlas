# Reference Build Benchmark Model

P3 turns ATLAS from a capability catalog into a system that can be tested against complete product briefs.

The benchmark does not treat static repository checks as proof that a live AI runtime can build a production product. It separates:

1. **Harness validity** — fixtures, scoring, blockers, schemas, and reports are deterministic and CI-verifiable.
2. **Live execution quality** — a Claude Code, Codex, or other runtime actually builds the reference product and produces inspectable evidence.
3. **Cross-runtime comparison** — equivalent briefs and scoring rules are compared only after each live run has independent review evidence.

## Canonical principle

**The benchmark scores evidence, not confidence; a green harness is not a green product.**

## Reference builds

P3 defines three deliberately different products:

- `premium-marketing-site`: visual authorship, conversion, content, public-web quality, browser behavior, and performance.
- `multitenant-subscription-saas`: identity, tenancy, billing, distributed state, operational primitives, premium product UI, and failure recovery.
- `internal-operations-system`: dense operational UX, privileged workflows, search/filtering, auditability, bulk operations, and safe administrative behavior.

These are product briefs, not source-code templates. A runtime may choose different implementation stacks when the brief and ATLAS gates justify them.

## Benchmark axes

Every reference build is scored on the same ten axes with build-specific weights:

1. Brief Fidelity
2. Architecture Quality
3. Capability Routing
4. Implementation Completeness
5. Frontend Craft
6. Security & Isolation
7. Failure Resilience
8. Browser Reality
9. Production Readiness
10. Independent Review

Weights sum to 100 for each build. Each axis contains deterministic checks. Check status factors are defined by the rubric and converted into weighted scores.

## Blocking policy

A high aggregate score cannot hide a release-blocking defect.

Each reference build declares blocking checks. Any blocking check that is not `pass` forces the benchmark outcome to `blocked`, regardless of numeric score. Independent review outcomes `Changes required` and `Blocked` also force `blocked`.

## Claim policy

`harness-smoke` runs exist only to prove that the benchmark engine, fixtures, and reports work. They are never claimable as product-quality results.

A result may be marked `claimable=true` only when:

- `execution_mode` is `live`;
- the submission identifies the runtime, model, repository, commit, and evidence root;
- every scored `pass` or `partial` check cites inspectable evidence;
- no blocking check failed or remains unverified;
- independent review is present and does not block release.

Even a claimable result is evidence for that exact run, model, commit, environment, and fixture. It is not a universal model ranking.

## Runtime fairness

Claude Code and Codex comparisons must use:

- the same fixture version;
- the same benchmark rubric version;
- equivalent tool/network permissions where practical;
- the same allowed starting assets;
- the same acceptance criteria and prohibited shortcuts;
- separately captured run metadata and costs/time when available.

If execution environments materially differ, the comparison report must disclose the difference.

## Anti-gaming rules

- Do not mark a check `pass` without a concrete evidence reference.
- Do not use benchmark fixture text as a substitute for implementing the required product behavior.
- Do not award production-readiness credit for screenshots without functional evidence.
- Do not award security/isolation credit from architecture prose alone when negative tests are required.
- Do not award Frontend Craft credit from a design description alone when rendered evidence is required.
- Do not silently omit failed or unimplemented checks.
- Do not convert a harness-smoke score into a public product benchmark claim.

## P3 feedback loop

After every live reference build:

1. record axis/check failures;
2. classify each failure as implementation error, routing error, missing capability, workflow weakness, evidence gap, or fixture ambiguity;
3. prefer improving an existing skill/workflow before adding a new agent;
4. re-run the same fixture after remediation;
5. compare the new result against the prior run without rewriting the historical result.

This keeps ATLAS growth evidence-driven rather than catalog-driven.
