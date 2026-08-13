# Capability Quality Post-P1 — 2026-08-13

This measurement uses the same deterministic evaluators as the pre-P1 baseline after adding the seven P1 skills. Static metrics remain diagnostic proxies rather than live-runtime accuracy claims.

## Inventory

- Skills: **117** (baseline 110; delta +7)
- Agent surfaces: **87**
- Agent pairs: **3741**
- Curated routing fixtures: **31**

## Skill quality

- Mean: **88.15** (baseline 87.44; delta +0.71)
- Median: **88** (baseline 86.0; delta +2.00)
- Minimum: **60** (baseline 60)
- P25: **86.0**
- P75: **90.0**
- Grades: **{'A': 34, 'B': 73, 'C': 9, 'D': 1}**

## Routing proxy

- Curated top-1: **74.2%** (baseline 70.8%)
- Curated top-3: **87.1%** (baseline 83.3%)
- Curated top-5: **93.5%** (baseline 91.7%)
- Description pairs >= 0.55: **1** (baseline 1)
- Description pairs >= 0.70: **0**

Self-retrieval remains a diagnostic lexical experiment only and is not used as a blocking release threshold.

## Agent overlap

- Pairs >= 0.55: **0** (baseline 0)
- Pairs >= 0.70: **0**
- Cross-domain pairs >= 0.55: **0** (baseline 0)

## Post-P1 decision

P1 preserves the no-agent-inflation policy because the agent surface remains 87 and no new agent was introduced. Any material regression in curated routing, description collisions, or agent-overlap must be inspected before the next capability expansion.
