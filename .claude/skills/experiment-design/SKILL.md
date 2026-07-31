---
name: experiment-design
description: "Design an experiment with explicit hypothesis, metrics, population, analysis, and decision rules."
---

# Experiment Design Skill

## Purpose

Design an experiment with explicit hypothesis, metrics, population, analysis,
and decision rules.

## Inputs

- Product uncertainty
- Candidate change
- Available traffic or sample
- Business constraints

## Procedure

1. State the hypothesis.
2. Define treatment and control.
3. Define primary metric.
4. Define guardrail metrics.
5. Define population and exclusions.
6. Estimate sample and duration assumptions.
7. Define analysis and stopping rules.
8. Identify bias, privacy, and ethical risks.

## Output

- Experiment brief
- Metrics
- Population
- Duration assumptions
- Analysis plan
- Decision rules
- Risks

## Domain

The skill covers the project and engineering context described by its purpose: Design an experiment with explicit hypothesis, metrics, population, analysis, and decision rules.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Design an experiment with explicit hypothesis, metrics, population, analysis, and decision rules.
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
