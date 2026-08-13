# ATLAS Reference Build Benchmark

P3 evaluates whether ATLAS can turn fixed product briefs into complete, evidence-backed products.

## Suite

- `premium-marketing-site.yaml` — premium public web experience and conversion quality.
- `multitenant-subscription-saas.yaml` — tenant isolation, billing, distributed state, operational primitives, and product UI.
- `internal-operations-system.yaml` — dense operational UX, privileged workflows, auditability, and bulk operations.

The briefs are under `specs/`. They are intentionally fictional and stack-agnostic.

## Scoring

All builds use ten shared axes but different weights. The fixture defines the checks and blockers; `scoring-rubric.yaml` defines status factors, score thresholds, independent-review behavior, and claim policy.

`pass = 1.0`, `partial = 0.5`, `fail = 0`, and `unverified = 0`.

A blocking check that is anything other than `pass` makes the run `blocked`, even when the numeric score is high.

## Live run

Create a submission matching `submission.schema.json` and score it:

```bash
python scripts/run_reference_build_benchmark.py \
  --spec benchmarks/reference-builds/specs/premium-marketing-site.yaml \
  --submission path/to/live-submission.yaml \
  --output path/to/result.json
```

A `live` result must identify runtime, model, repository, commit, evidence root, and independent review. Evidence references must be inspectable and may not use the synthetic harness scheme.

## Harness smoke

The files under `examples/` deliberately mark every fixture check as passed using synthetic references. They exist only to prove that parsing, blockers, scoring, and output work in CI.

Run all smoke fixtures:

```bash
python scripts/run_reference_build_benchmark.py --suite-smoke
```

Harness scores are always `claimable=false` and `outcome=harness-only`.

## Runtime comparison

After independently scoring two runs of the exact same fixture/rubric:

```bash
python scripts/run_reference_build_benchmark.py \
  --compare claude-result.json codex-result.json \
  --output comparison.json
```

The comparison is diagnostic when either input is non-claimable.

## Evidence layout recommendation

A live reference-build repository should keep a stable evidence root containing browser screenshots/traces, test output, architecture decisions, security/tenant negative tests, provider/reconciliation evidence, performance/search evidence where applicable, and the independent review.

The benchmark does not require one vendor-specific directory shape. It requires evidence to be concrete, reviewable, and tied to the exact run commit.
