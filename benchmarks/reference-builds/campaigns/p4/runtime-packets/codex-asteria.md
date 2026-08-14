# P4 Asteria Target Packet - Codex

Execute the canonical `premium-marketing-site` fixture as an isolated Codex target run from the exact campaign base commit.

Do not inspect, fetch, diff, or reuse implementation/evidence/results from any other `bench/p4-asteria-*` branch. Do not search repository history for an Asteria solution.

Follow `site-from-brief-delivery` and inherited Frontend Craft, browser, accessibility, responsive, SEO, structured-data, analytics/conversion, supply-chain, production, and independent review gates.

Before implementation, record runtime as `codex`, the model string exactly as Codex reports it at run time, and freeze the P4.1 environment capability manifest using `scripts/capture_benchmark_environment.py`. Do not infer browser or deployment availability from source configuration.

If the runtime cannot produce browser evidence itself, use the campaign-owned portable browser workflow and label the source `campaign-portable`; never present fallback evidence as runtime-native evidence.

Before scoring, produce an evidence-assurance sidecar matching `benchmarks/reference-builds/campaigns/p4/assurance/evidence-assurance.schema.json` and pass `scripts/validate_benchmark_evidence_assurance.py`. In particular, verify non-text contrast, 404 robots/canonical behavior, visual-regression mode, recovery claims, mutable-content cache freshness, evidence-reference existence, and public HTTPS deployment truth.

Freeze the first result before remediation. Independent review must be performed by a reviewer that did not implement the build.
