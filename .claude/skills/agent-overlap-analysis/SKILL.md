---
name: agent-overlap-analysis
description: "Measure semantic overlap across registered ATLAS agents when roles are added, scopes change, or the catalog may contain redundant responsibilities, using descriptions, missions, ownership, and taxonomy boundaries."
---

# Agent Overlap Analysis

## Purpose

Detect agent scopes that are becoming difficult to distinguish before ATLAS responds by adding more personas or allowing routing ambiguity to accumulate.

## Trigger conditions

Use before adding a new agent, after material agent-scope edits, during catalog audits, or when multiple agents appear eligible for the same durable responsibility.

## Inputs

- Registered agent files
- Canonical agent descriptions
- Mission and ownership/responsibility sections
- `framework/capabilities/agent-taxonomy.yaml`
- Prior overlap baseline when available

## Procedure

1. Run `python scripts/analyze_agent_overlap.py`.
2. Build a deterministic semantic proxy from description, mission, ownership/responsibility, and domain membership.
3. Rank agent pairs by weighted lexical similarity.
4. Distinguish expected same-domain adjacency from suspicious cross-domain or near-duplicate ownership.
5. Inspect high-scoring pairs manually and compare their actual decision authority and required outputs.
6. Prefer clarifying boundaries, moving a repeatable procedure into a skill, or consolidating roles before adding another overlapping agent.
7. Treat exact or near-exact purpose duplication as blocking catalog debt.
8. Record accepted adjacency when two roles intentionally cooperate but retain distinct durable outcomes.

## Outputs

- Total agents measured
- Highest-overlap pairs
- Same-domain and cross-domain overlap summaries
- Candidate redundant roles
- Boundary-clarification recommendations
- Baseline comparison

## Dependencies

- Python 3
- PyYAML
- Canonical registry, taxonomy, and agent files
- `scripts/analyze_agent_overlap.py`

## Limitations

- Lexical similarity cannot determine organizational correctness by itself.
- Specialized agents may share vocabulary while owning different decisions.
- Low lexical overlap does not prove role boundaries are clear.

## Validation

- Confirm the measured agent count equals the canonical orchestrator plus registered specialist agents.
- Verify taxonomy membership resolves for every measured agent.
- Run twice on the same commit and verify deterministic pair ordering.
- Manually inspect the highest-overlap pairs before changing role ownership.
