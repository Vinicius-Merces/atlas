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

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
