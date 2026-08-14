# P4 Asteria Target Packet - Claude Code

Execute the canonical `premium-marketing-site` fixture as an isolated Claude Code target run from the exact campaign base commit.

Do not inspect, fetch, diff, or reuse implementation/evidence/results from any other `bench/p4-asteria-*` branch. Do not search repository history for an Asteria solution.

Follow `site-from-brief-delivery` and inherited Frontend Craft, browser, accessibility, responsive, SEO, structured-data, analytics/conversion, supply-chain, production, and independent review gates.

Before implementation, record runtime as `claude-code`, the model string exactly as Claude Code reports it at run time, and freeze the environment capability manifest using `scripts/capture_benchmark_environment.py`. The run manifest must also reserve paths for the evidence-assurance and deployment-evidence sidecars. Do not infer browser or deployment availability from source configuration.

If the runtime cannot produce browser evidence itself, use the campaign-owned portable browser workflow and label the source `campaign-portable`; never present fallback evidence as runtime-native evidence.

For public deployment evidence, use the campaign-owned controlled deployment workflow `.github/workflows/reference-build-controlled-deployment.yml` against the frozen implementation ref when native hosting is unavailable or would create target-specific infrastructure. Record the result as `controlled-preview`. A controlled preview is real public HTTPS evidence but **must not** be used to mark `marketing-production-domain` as pass. Only an enabled campaign-owned `claimable-production` adapter may satisfy that blocker.

Before scoring, produce an evidence-assurance sidecar matching `benchmarks/reference-builds/campaigns/p4/assurance/evidence-assurance.schema.json` and pass `scripts/validate_benchmark_evidence_assurance.py`. Produce deployment evidence matching `benchmarks/reference-builds/campaigns/p4/controlled-deployment/deployment-evidence.schema.json` and pass `scripts/validate_controlled_deployment_evidence.py`. In particular, verify non-text contrast, 404 robots/canonical behavior, visual-regression mode, recovery claims, mutable-content cache freshness, evidence-reference existence, and deployment-class truth.

Freeze the first result before remediation. Independent review must be performed by a reviewer that did not implement the build.
