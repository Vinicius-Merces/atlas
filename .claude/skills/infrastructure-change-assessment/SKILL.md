---
name: infrastructure-change-assessment
description: "Evaluate the operational risk of infrastructure or deployment changes."
---

# Infrastructure Change Assessment Skill

## Purpose

Evaluate the operational risk of infrastructure or deployment changes.

## Inputs

- Proposed infrastructure change
- Current environment topology
- Deployment model
- Recovery requirements

## Procedure

1. Identify affected resources and environments.
2. Determine dependency and blast radius.
3. Check configuration and secret impact.
4. Assess deployment ordering.
5. Identify rollback limitations.
6. Define monitoring and validation.
7. Recommend approval conditions.

## Output

- Change scope
- Blast radius
- Risks
- Deployment sequence
- Validation
- Rollback strategy

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
