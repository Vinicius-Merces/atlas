# Reference Build Benchmark Workflow

## Trigger

Run when ATLAS needs to prove end-to-end construction quality against a fixed reference brief, compare Claude Code and Codex on equivalent work, or investigate whether a framework change improved or regressed complete-product delivery.

## Objective

Execute one canonical reference build from a clean starting state, capture evidence for every required benchmark check, obtain independent review, score the run deterministically, and preserve the result without confusing harness validation with live-model capability.

## Inputs

- A versioned reference-build fixture under `benchmarks/reference-builds/specs/`.
- `benchmarks/reference-builds/scoring-rubric.yaml`.
- Runtime/model identity and execution environment.
- Starting repository/commit or other explicitly allowed starting assets.
- Tool, network, provider, and credential permissions.
- Output repository/commit and deployed environment when the fixture requires deployment.
- Independent reviewer identity/runtime and evidence location.

## Sequence

1. Read `framework/reference-build-benchmark-model.md` and the selected fixture completely.
2. Record run metadata before implementation: fixture version, runtime/model, starting commit, permissions, environment, and allowed assets.
3. Execute the fixture's declared delivery workflow (`site-from-brief-delivery` or `saas-from-brief-delivery`) without weakening inherited Frontend Craft, trust, P1, P2, browser, or release gates.
4. Maintain a benchmark evidence ledger while building; every check eventually marked `pass` or `partial` must cite concrete evidence.
5. Capture negative/failure evidence for fixture blockers, not only happy-path screenshots.
6. Produce a submission YAML matching `benchmarks/reference-builds/submission.schema.json`.
7. Assign an independent reviewer who was not the sole implementer and run `.claude/reviews/reference-build-benchmark-review.md`.
8. Record the independent review outcome in the submission.
9. Score the run with `python scripts/run_reference_build_benchmark.py --spec <spec> --submission <submission> --output <result.json>`.
10. If comparing runtimes, score each run independently before using the runner's `--compare` mode.
11. Classify every failed/unverified check as implementation error, routing error, missing capability, workflow weakness, evidence gap, or fixture ambiguity.
12. Feed validated framework gaps back into the normal ATLAS capability/workflow process without rewriting historical benchmark results.

## Required lifecycle

1. **Understand** — read the fixed brief, benchmark rules, prohibited shortcuts, and success criteria.
2. **Inspect** — verify the starting state, allowed assets, runtime permissions, prior benchmark history, and applicable ATLAS gates.
3. **Plan** — select the delivery path, evidence strategy, negative tests, deployment target, reviewer, and run metadata.
4. **Execute** — build the complete product while preserving benchmark isolation and normal ATLAS engineering standards.
5. **Validate** — exercise every required check and blocking condition with inspectable evidence.
6. **Review** — perform independent benchmark review after implementation evidence exists.
7. **Document** — preserve submission, result, run metadata, evidence locations, residual risks, and framework-gap classification.
8. **Deliver** — publish the run result only when its claimability rules are satisfied; otherwise label it harness-only or non-claimable.

## Responsible agents

- `orchestrator`: starts the run, preserves fixture scope, and prevents benchmark shortcuts.
- `solution-blueprint-engineer`: maps the brief to the closest blueprint and delivery workflow without turning the fixture into a source template.
- Product/engineering specialists selected by the delivery workflow: implement the reference product.
- `qa-engineer` / `test-automation-engineer`: collect browser, failure, and regression evidence.
- `reference-implementation-reviewer`: independently judges completeness and instructional/architectural quality.
- `runtime-parity-reviewer`: compares Claude Code/Codex results only after both independent scores exist.

## Decision points

- Is this run `harness-smoke` or a genuine `live` execution?
- Are runtime permissions materially equivalent to earlier/comparison runs?
- Which fixture checks require deployed evidence rather than source inspection?
- Which blockers require direct negative testing?
- Is a missing check an implementation failure or an ambiguous fixture?
- Is the independent reviewer sufficiently separate from implementation?
- Is a framework change justified by repeated benchmark evidence rather than one isolated run?
- Can the result be marked claimable under the canonical model?

## Validation

- Validate fixtures and rubric with `python scripts/validate_reference_build_benchmark_pack.py`.
- Validate the submission schema and exact check set before scoring.
- Require evidence references for every `pass` and `partial`.
- Require all declared blocking checks to be `pass` for a non-blocked outcome.
- Preserve exact fixture/rubric version in the result.
- Run existing ATLAS release validation for framework changes caused by benchmark findings.
- When comparing runtimes, disclose environment/tool differences alongside score deltas.

## Failure handling

- Do not manufacture evidence to satisfy a check.
- Do not downgrade a blocking check because aggregate score is high.
- Do not call a harness-smoke result a live benchmark.
- Do not let the implementer self-approve the independent review gate.
- If deployment/provider access is unavailable, mark affected checks `unverified`; do not assume equivalence from local code.
- If a fixture is ambiguous, record `fixture-ambiguity` and repair the fixture before using that ambiguous check to rank runtimes.
- If a runtime run is interrupted, preserve the partial result instead of silently restarting under different conditions.

## Completion criteria

- The exact fixture and rubric versions are recorded.
- Every fixture check has a status and evidence/notes consistent with the schema.
- All blocking checks are explicitly resolved or cause a blocked result.
- Independent review is recorded.
- The deterministic scorer produces a reproducible JSON result.
- Claimability is stated explicitly.
- Any proposed ATLAS improvement is traceable to benchmark evidence rather than intuition alone.
