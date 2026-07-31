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

## Domain

The skill covers the project and engineering context described by its purpose: Choose the closest ATLAS blueprint for a project.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Choose the closest ATLAS blueprint for a project.
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
