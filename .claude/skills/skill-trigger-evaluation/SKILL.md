---
name: skill-trigger-evaluation
description: "Evaluate whether ATLAS skill discovery metadata and trigger conditions route representative requests to the intended capability without excessive collisions when skills are added, renamed, or overlap risk changes."
---

# Skill Trigger Evaluation

## Purpose

Measure whether skill discovery text is discriminative enough for routing and whether trigger language aligns with the canonical description instead of relying on subjective confidence.

## Trigger conditions

Use when skills are added, descriptions or trigger conditions change, routing ambiguity is suspected, a capability domain grows dense, or a release needs evidence that discovery quality has not regressed.

## Inputs

- Registered canonical skill descriptions
- `## Trigger conditions` sections
- Curated routing fixtures
- Capability taxonomy
- Prior routing baseline when available

## Procedure

1. Run `python scripts/evaluate_skill_routing.py`.
2. For every registered skill, compare its trigger language against all canonical discovery descriptions using the deterministic lexical retrieval proxy.
3. Record self-retrieval rank at top-1, top-3, and top-5.
4. Compute nearest-neighbor description similarity and flag unusually similar skill pairs for review.
5. Run curated routing fixtures that represent realistic, ambiguous, positive, and negative requests.
6. Inspect misses instead of automatically rewriting descriptions around the evaluator.
7. Use model/runtime behavioral evaluation separately when available; do not claim lexical retrieval is equivalent to Claude Code or Codex routing.
8. Pair high-collision results with `agent-overlap-analysis` when ambiguity may come from role ownership rather than skill wording.

## Outputs

- Self-retrieval top-1/top-3/top-5 rates
- Curated fixture top-k accuracy
- High-similarity skill pairs
- Missed or ambiguous routing cases
- Baseline comparison
- Recommended description/trigger refinements

## Dependencies

- Python 3
- PyYAML
- Canonical skill registry
- `tests/fixtures/capability-routing-cases.yaml`
- `scripts/evaluate_skill_routing.py`

## Limitations

- Lexical retrieval is a deterministic proxy, not a live LLM-routing benchmark.
- Synonyms and semantically correct but lexically distant phrasing may score lower.
- Curated fixtures must remain representative and must not be rewritten solely to improve metrics.

## Validation

- Confirm every registered skill participates in the self-retrieval measurement.
- Confirm curated fixture targets are registered canonical skills.
- Run twice on the same commit and verify identical ranking/summary output.
- Review top collision pairs manually before declaring two skills redundant.
