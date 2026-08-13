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
3. Record a run manifest before implementation begins.
4. Give the runtime only the canonical fixture, ATLAS framework surfaces, and its runtime packet.
5. Execute the fixture's declared delivery workflow.
6. Collect browser, architecture, test, security, failure, SEO/performance, and deployment evidence required by the fixture.
7. Freeze the implementation/evidence commit.
8. Produce a live benchmark submission tied to that commit.
9. Obtain an independent review that did not implement the build.
10. Score the submission with the P3 scorer.
11. Remediate only after the first frozen result is preserved.
12. Repeat on a new commit if needed, preserving before/after results.
13. Compare target runs only after both are frozen on the exact same fixture and rubric.

## Evidence rules

Evidence must be concrete and inspectable. Examples include browser screenshots/traces, automated test output, deployment URLs, HTTP/SEO probes, accessibility findings, performance measurements, architecture decisions, negative authorization/form tests, provider/reconciliation records, and independent review findings.

A statement in a report is not evidence by itself when the underlying behavior can be tested directly.

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

Calibration can still be useful under those conditions, but it must be labeled diagnostic.

## P4 completion

P4 is complete when campaign infrastructure is validated and merged, a diagnostic calibration has exercised the live path, Codex and Claude Code target runs are independently frozen, and the exact-fixture comparison plus remediation backlog are recorded.
