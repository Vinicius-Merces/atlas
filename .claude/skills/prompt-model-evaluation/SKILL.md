---
name: prompt-model-evaluation
description: "Compare prompt, model, retrieval, or tool configurations using repeatable evaluation scenarios."
---

# Prompt and Model Evaluation Skill

## Purpose

Compare prompt, model, retrieval, or tool configurations using repeatable
evaluation scenarios.

## Inputs

- Candidate configurations
- Evaluation scenarios
- Expected outcomes
- Quality thresholds
- Cost and latency constraints

## Procedure

1. Define scoring criteria.
2. Separate development and holdout scenarios.
3. Run candidates consistently.
4. Record quality, failure, latency, and cost.
5. Analyze regressions and edge cases.
6. Recommend configuration and fallback.

## Output

- Evaluation design
- Results
- Failure examples
- Recommendation
- Limitations

## Domain

The skill covers the project and engineering context described by its purpose: Compare prompt, model, retrieval, or tool configurations using repeatable evaluation scenarios.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Compare prompt, model, retrieval, or tool configurations using repeatable evaluation scenarios.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository or runtime inspection and validation capabilities required by the procedure.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
