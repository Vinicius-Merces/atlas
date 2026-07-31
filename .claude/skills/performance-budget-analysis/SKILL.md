---
name: performance-budget-analysis
description: "Define and evaluate measurable performance limits."
---

# Performance Budget Analysis Skill

## Purpose

Define and evaluate measurable performance limits.

## Inputs

- User journey
- Current baseline
- Platform constraints
- Business criticality

## Possible budgets

- Response latency
- Error rate
- Throughput
- Memory use
- CPU use
- Bundle size
- Startup time
- Largest Contentful Paint
- Interaction latency
- Database query duration

## Output

- Baseline
- Proposed budgets
- Measurement method
- Regression threshold
- Blocking threshold
- Review cadence

## Domain

The skill covers the project and engineering context described by its purpose: Define and evaluate measurable performance limits.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Define and evaluate measurable performance limits.
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
