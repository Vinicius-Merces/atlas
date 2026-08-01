---
name: blueprint-selection
description: "Choose the closest ATLAS blueprint for a project."
---

# Blueprint Selection Skill

## Purpose

Choose the closest ATLAS blueprint for a project.

## Inputs

- Product type
- Users
- Architecture
- Data sensitivity
- Integrations
- Availability needs
- Team constraints

## Output

- Recommended blueprint
- Fit assessment
- Required adaptations
- Unsupported assumptions
- Additional agents and workflows

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
