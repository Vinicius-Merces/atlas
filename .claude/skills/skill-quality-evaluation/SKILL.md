---
name: skill-quality-evaluation
description: "Measure registered ATLAS skills for structural completeness, discovery quality, trigger clarity, evidence strength, boundaries, and context discipline when the capability library changes or quality must be baselined."
---

# Skill Quality Evaluation

## Purpose

Measure the quality of every registered skill with reproducible repository evidence instead of judging prompt quality by file count or intuition.

## Trigger conditions

Use when skills are added or changed, before capability-pack expansion, during framework audits, or when ATLAS needs a comparable quality baseline across the complete skill inventory.

## Inputs

- `.claude/registry.json`
- Canonical `.claude/skills/*/SKILL.md` files
- `.claude/contracts/skill-contract.md`
- Current capability taxonomy and discovery rules
- Prior evaluation baseline when available

## Procedure

1. Run `python scripts/evaluate_skill_quality.py`.
2. Score every registered skill across metadata/discovery, required structure, trigger quality, validation/evidence, declared boundaries/dependencies, and context discipline.
3. Treat the score as a diagnostic composite, not as proof that a skill behaves correctly in a live model.
4. Inspect the lowest-scoring skills and the reasons attached to each dimension.
5. Separate structural failures from quality opportunities. Missing contract-required material is a correctness issue; a merely lower but valid score is improvement work.
6. Compare aggregate score, distribution, and bottom quartile against the prior baseline before changing thresholds.
7. Pair this result with `skill-trigger-evaluation`; a well-written skill that cannot be routed reliably is not high quality.
8. Record any accepted quality debt explicitly rather than weakening the evaluator to hide it.

## Outputs

- Total registered skills measured
- Mean, median, minimum, and percentile score
- Grade distribution
- Per-skill dimension scores and reasons
- Lowest-scoring skills requiring improvement
- Baseline comparison and regression findings

## Dependencies

- Python 3
- PyYAML from `requirements-test.txt`
- Canonical registry and skill files
- `scripts/evaluate_skill_quality.py`

## Limitations

- Static scoring cannot prove usefulness, factual correctness, or live-model behavior.
- Word-count and lexical signals are proxies and must not reward verbosity for its own sake.
- Thresholds should only become blocking after a measured baseline exists.

## Validation

- Confirm the evaluator measures exactly the registered skill count.
- Run the evaluator twice on the same commit and verify deterministic output.
- Confirm a deliberately malformed fixture loses points in the expected dimensions.
- Review at least the bottom five skills manually before changing a global threshold.
