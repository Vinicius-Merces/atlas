# Reference Build Benchmark Capability Map

## Purpose

P3 is ATLAS's end-to-end proving ground. It tests whether the existing capability system can turn a fixed brief into a complete product and produce evidence strong enough for independent scoring.

## Canonical sources

- Model: `framework/reference-build-benchmark-model.md`
- Overlay: `framework/capabilities/reference-build-benchmark.yaml`
- Workflow: `.claude/workflows/reference-build-benchmark.md`
- Review: `.claude/reviews/reference-build-benchmark-review.md`
- Suite: `benchmarks/reference-builds/`
- Runner: `scripts/run_reference_build_benchmark.py`
- Validator: `scripts/validate_reference_build_benchmark_pack.py`

## Reference builds

- Premium Marketing Site — tests brand-specific Frontend Craft, conversion, content, SEO, browser behavior, performance, and production web evidence.
- Multi-Tenant Subscription SaaS — tests architecture, identity, isolation, billing, distributed state, P2 operational primitives, recovery, and premium application UI.
- Internal Operations System — tests dense UX, privileged operations, auditability, search/filtering, bulk workflows, safe destructive actions, and operational responsiveness.

## Interpretation

A green P3 harness proves that ATLAS can validate fixtures and score submissions deterministically.

It does **not** prove that a model built the reference product.

Only a versioned `live` submission with inspectable evidence and independent review may become a claimable benchmark result.

## Feedback rule

Benchmark failures should normally improve an existing skill, workflow, fixture, or evidence gate first. Add a new durable agent only when repeated evidence shows a genuinely distinct responsibility.
