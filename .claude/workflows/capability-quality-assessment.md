# Capability Quality Assessment Workflow

## Trigger

The capability catalog is about to expand, skills or agent scopes changed materially, routing ambiguity is suspected, or a release needs a measured capability-quality baseline.

## Objective

Measure the complete registered skill and agent catalog, identify quality/routing/overlap debt, and make evidence-based decisions before adding more capabilities.

## Inputs

- Canonical registry
- Agent taxonomy
- Skill and agent contracts
- Registered skill/agent files
- Routing fixtures
- Prior measurement baseline when available

## Sequence

1. Read `framework/capability-evaluation-model.md`.
2. Run `skill-quality-evaluation` across every registered skill.
3. Run `skill-trigger-evaluation` across every registered skill plus curated routing fixtures.
4. Run `agent-overlap-analysis` across the orchestrator and specialist agents.
5. Inspect bottom-quality skills, routing misses, and highest-overlap pairs.
6. Classify each finding as structural defect, routing ambiguity, expected adjacency, improvement opportunity, or accepted limitation.
7. Resolve blocking defects before expanding the catalog.
8. Complete independent `capability-quality-review`.
9. Record the baseline summary and use it to compare the next capability pack.

## Required lifecycle

1. Understand what changed in the capability surface.
2. Measure the complete canonical inventory.
3. Inspect outliers and collisions.
4. Correct defects without gaming metrics.
5. Re-run deterministic measurements.
6. Review independently.
7. Record baseline and residual limitations.

## Responsible agents

- `technical-auditor`: primary evidence owner for skill-quality measurement.
- `task-routing-engineer`: primary owner for trigger/routing analysis.
- `orchestrator`: owns agent-boundary and catalog-shape decisions.
- `runtime-catalog-maintainer`: consulted when generated discovery surfaces are affected.
- independent reviewer: verifies the measurement claims and interpretation.

## Validation

- Run `python scripts/evaluate_skill_quality.py`.
- Run `python scripts/evaluate_skill_routing.py`.
- Run `python scripts/analyze_agent_overlap.py`.
- Confirm skill and agent counts match the registry/taxonomy.
- Confirm repeated execution on the same commit is deterministic.
- Run `python scripts/validate_capability_evaluation_pack.py`.
- Complete `capability-quality-review`.

## Failure handling

- Do not hide poor results by lowering a threshold without documenting the measured baseline and rationale.
- Do not convert every collision into a new agent.
- Do not treat lexical routing or overlap metrics as live-model accuracy.
- Do not proceed with a new capability pack if contract-required skill structure is broken.

## Completion criteria

- Every registered skill was measured.
- Every agent was included in overlap analysis.
- Curated routing fixtures are valid and executed.
- Outliers are classified.
- Blocking defects are resolved.
- Baseline metrics and limitations are recorded.
- Independent review is complete.
