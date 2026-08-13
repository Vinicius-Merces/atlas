# Capability Quality Baseline — 2026-08-13

This document records the first full ATLAS capability-quality measurement before P1 expansion.

## Scope

Measured commit lineage: Capability Evaluation Pack stacked on Web Production Assurance.

Measured inventory:

- 87 agent surfaces, including the orchestrator
- 110 registered skills
- 3,741 unique agent pairs
- 24 curated skill-routing cases

The metrics below are deterministic static diagnostics. They are not claims about live Claude Code or Codex model accuracy.

## Skill quality baseline

`python scripts/evaluate_skill_quality.py`

- Mean: **87.44 / 100**
- Median: **86.0**
- Minimum: **60**
- P25: **86.0**
- P75: **88.0**
- Grade A: **27**
- Grade B: **73**
- Grade C: **9**
- Grade D: **1**

Lowest-scoring skills at baseline:

1. `accessibility-audit` — 60
2. `runtime-semantic-parity` — 71
3. `adapter-drift-detection` — 73
4. `localization-readiness-assessment` — 73
5. `mobile-architecture-assessment` — 73
6. `rag-architecture-assessment` — 73
7. `reference-implementation-review` — 73
8. `architecture-audit` — 75
9. `content-quality-review` — 75
10. `release-integrity-verification` — 75

Interpretation: the catalog is structurally healthy enough to expand, but legacy compact skills remain a quality-improvement backlog. `accessibility-audit` is the only D-grade skill and should be modernized without gaming the evaluator.

## Skill routing baseline

`python scripts/evaluate_skill_routing.py`

Self-retrieval, using each skill's trigger conditions as a lexical query against canonical descriptions:

- Top-1: **14.5%**
- Top-3: **20.9%**
- Top-5: **22.7%**

Curated realistic routing fixtures:

- Top-1: **70.8%**
- Top-3: **83.3%**
- Top-5: **91.7%**

Description-collision signals:

- Similarity >= 0.55: **1 pair**
- Similarity >= 0.70: **0 pairs**
- Highest pair: `privacy-impact-assessment` / `threat-modeling` at **0.56**

Interpretation: self-retrieval is intentionally not a release threshold. Trigger sections and compact runtime descriptions serve different purposes and often use different vocabulary. The curated fixtures are a better static routing signal, while still remaining a lexical proxy rather than a live-runtime benchmark.

## Agent overlap baseline

`python scripts/analyze_agent_overlap.py`

- Agent surfaces: **87**
- Unique pairs: **3,741**
- Similarity >= 0.55: **0**
- Similarity >= 0.70: **0**
- Cross-domain similarity >= 0.55: **0**

Highest observed pairs:

- `beta-release-coordinator` / `stability-engineer`: 0.41
- `security-engineer` / `threat-modeling-engineer`: 0.40
- `data-engineer` / `privacy-engineer`: 0.32
- `cloud-architect` / `finops-engineer`: 0.31
- `audit-bundle-reviewer` / `evidence-ledger-architect`: 0.31

Interpretation: there is no measured evidence that P1 requires new specialist agents. P1 capabilities should therefore be implemented as skills routed through existing durable roles.

## P1 admission decision

**Approved with conditions.**

P1 may proceed because:

- all registered capabilities were included in the measurement;
- no agent pair crossed the review threshold;
- description collisions are minimal;
- curated routing is strong at top-5;
- capability contracts and evaluation infrastructure are explicit.

Conditions:

- do not introduce new P1 agents without a new overlap analysis and durable-responsibility justification;
- re-run the same measurements after P1 and compare against this baseline;
- treat static metrics as diagnostic evidence, never as live runtime accuracy;
- keep legacy low-scoring skills visible as improvement debt rather than lowering quality thresholds to conceal them.
