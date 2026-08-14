# Live Reference Build Campaign Model

P4 turns the P3 benchmark harness into a controlled live-build campaign.

The purpose is not to create a hidden reference implementation. The purpose is to let multiple runtimes receive the same frozen brief, build independently, preserve inspectable evidence, and produce benchmark results that can be compared without implementation leakage.

## Campaign principle

**Same brief, same rubric, isolated implementation, real runtime identity, inspectable evidence, independent review.**

A live campaign result is evidence about one runtime/model/tool environment at one commit. It is not a universal claim about the runtime family.

## Isolation rules

Every target run starts from the same recorded campaign base commit.

Each run uses its own branch or repository. A runtime must not inspect, copy, diff, or reuse another target run's implementation, evidence, score, review, screenshots, or remediation notes before its own result is frozen.

The campaign branch in `main` contains only fixture, protocol, packets, validators, and campaign metadata. It must not contain the solution that a target runtime is expected to build.

After all target results are frozen, implementations and evidence may be compared by reviewers.

## Run classes

### Calibration

A calibration run proves the live campaign machinery against a real build but is not substituted for a declared target runtime.

Calibration results may reveal fixture ambiguity, evidence gaps, deployment friction, or scorer weaknesses. They may not be relabeled as Codex or Claude Code results.

### Target

Target runs are the runtime/model executions intended for public comparison.

For P4 the primary targets are Codex and Claude Code. Each target records the exact model string reported by the runtime at execution time rather than assuming a model name in advance.

## Required lifecycle

1. Freeze the campaign base commit, fixture SHA, and rubric SHA.
2. Create one isolated run branch/repository from that exact base.
3. Record a run manifest before implementation begins, including planned paths for environment, evidence-assurance, and deployment sidecars.
4. Freeze an environment capability manifest before implementation begins.
5. Give the runtime only the canonical fixture, ATLAS framework surfaces, and its runtime packet.
6. Execute the fixture's declared delivery workflow.
7. Collect architecture, test, security, failure, SEO/performance, and conversion evidence required by the fixture.
8. If native browser evidence is unavailable, use the campaign-owned portable browser fallback and label its source explicitly.
9. Produce public HTTPS evidence through the campaign-owned controlled deployment adapter when native deployment is unavailable or would differ across targets.
10. Record the deployment class explicitly as `controlled-preview`, `claimable-production`, or `unavailable`.
11. Produce and validate the evidence-assurance sidecar before scoring.
12. Freeze the implementation/evidence commit.
13. Produce a live benchmark submission tied to that commit.
14. Obtain an independent review that did not implement the build.
15. Score the submission with the P3 scorer.
16. Remediate only after the first frozen result is preserved.
17. Repeat on a new commit if needed, preserving before/after results.
18. Compare target runs only after both are frozen on the exact same fixture and rubric.

## Evidence rules

Evidence must be concrete and inspectable. Examples include browser screenshots/traces, automated test output, deployment URLs, HTTP/SEO probes, accessibility findings, performance measurements, architecture decisions, negative authorization/form tests, provider/reconciliation records, and independent review findings.

A statement in a report is not evidence by itself when the underlying behavior can be tested directly.

Every evidence reference used by an assurance sidecar must resolve to a repository path. A missing path is an evidence-integrity failure rather than a documentation typo.

## Environment normalization

P4.1 separates implementation quality from runtime tool availability.

Before implementation, every run freezes browser, deployment, network, command/runtime, and independent-review availability in an environment capability manifest. The manifest must state whether browser evidence comes from the runtime itself, the campaign-owned portable fallback, or remains unavailable.

Cross-runtime reports must preserve the observed raw score and the environment capability differences side by side. The campaign must not silently normalize a score by guessing what a runtime would have achieved with different tools.

## Browser evidence fallback

A campaign-owned GitHub Actions workflow may collect a minimum browser evidence floor from a frozen target ref when the coding runtime lacks Chromium or a browser bridge. The fallback may inspect public routes, multiple viewports, console errors, page errors, request failures, overflow, screenshots, canonicals, robots directives, and a real 404.

Fallback evidence is labeled `campaign-portable`. Product-specific flows, authentication, authoritative mutations, negative business states, and other fixture-specific behavior still require dedicated execution evidence.

## Assurance truth checks

P4.1 adds deterministic checks for failure modes observed in the first Asteria campaign:

- essential non-text control boundaries must meet the declared 3:1 minimum;
- 404 responses must return 404, include `noindex`, avoid conflicting index directives, and avoid canonicalising the error document to another page;
- screenshot capture may be labeled `capture-only`, but only a deterministic baseline plus diff report may be labeled visual regression;
- advertised retry, queue, reconciliation, or recovery behavior must cite both an implementation path and execution evidence;
- shared caches for mutable content must stay within an explicit freshness budget;
- public deployment claims require a real HTTPS URL plus evidence;
- source/configuration alone cannot upgrade an unavailable browser or deployment blocker.

## Controlled public deployment

P4.2 provides a campaign-owned public ingress path that does not depend on the coding runtime's hosting account or network permissions.

The default `controlled-preview` adapter runs the frozen build on a GitHub Actions runner and exposes the application through a pinned Cloudflare Quick Tunnel. The workflow records the exact source commit, public HTTPS URL, TLS protocol/certificate metadata, HTTP response headers/body hash, provider identity, start/finish timestamps, and cleanup policy. Portable Chromium evidence may then run against that public URL.

This layer exists to normalize externally reachable browser, network, SEO, crawl, and TLS evidence. It is real public HTTPS evidence, but it is temporary campaign infrastructure rather than a production deployment.

A `controlled-preview` must therefore remain `claimable_production=false`. It can improve confidence in browser/network/deployed-crawl behavior, but it cannot mark a fixture's production-domain blocker as pass.

## Claimable production separation

Production evidence is a distinct deployment class.

A `claimable-production` adapter must provide a persistent provider deployment tied to the frozen source commit, HTTPS, environment configuration evidence, inspectable deployment/runtime logs, and the same provider topology for every compared target. Credentials belong to the campaign deployment runner and must not be granted selectively to a target runtime.

The first supported provider shape is Vercel CLI/API deployment. It remains disabled until a campaign-owned project and credentials can be configured once and used identically for every target. The framework must prefer an honest controlled preview over a target-specific production deployment that would reintroduce environment bias.

## Frontend standard

The P4 marketing-site target inherits Frontend Craft in full. Premium means authored visual direction, hierarchy, responsive quality, accessible interaction, purposeful motion, strong content presentation, and conversion clarity. Generic luxury conventions, decorative excess, or screenshot-only polish do not satisfy the benchmark.

## Claim policy

A result is not comparison-grade when any of the following is true:

- runtime/model identity is guessed;
- another target implementation was visible or reused;
- the production-domain blocker is unverified;
- independent review was performed by the implementer;
- evidence is synthetic, missing, or detached from the run commit;
- fixture or rubric differs between compared runs.

A controlled public preview does not remove the production-domain requirement. Calibration can still be useful under non-claimable conditions, but it must be labeled diagnostic.

## P4 completion

P4 is complete when campaign infrastructure is validated and merged, a diagnostic calibration has exercised the live path, Codex and Claude Code target runs are independently frozen, and the exact-fixture comparison plus remediation backlog are recorded.

## P4.1 completion

P4.1 is complete when the benchmark can freeze environment capabilities before implementation, use a runtime-neutral browser fallback without falsifying evidence provenance, validate assurance sidecars deterministically, catch the measured Asteria evidence-integrity failures, and pass the normal ATLAS contract/release gates without adding benchmark-only agents or skills.

## P4.2 completion

P4.2 is complete when a frozen ref can be exposed through the same campaign-owned public HTTPS preview path regardless of runtime, that path produces schema-valid TLS/HTTP/source/lifecycle evidence, portable browser evidence can target the public URL, the controlled preview is deterministically prevented from masquerading as production, and the external ingress smoke plus normal ATLAS contract/release gates pass.
