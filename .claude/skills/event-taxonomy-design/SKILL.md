---
name: event-taxonomy-design
description: "Design stable, privacy-aware analytics events and properties."
---

# Event Taxonomy Design Skill

## Purpose

Design stable, privacy-aware analytics events and properties.

## Inputs

- Product journeys
- Measurement goals
- Existing events
- Identity model

## Procedure

1. Identify decisions the data should support.
2. Map meaningful user and system actions.
3. Define event names and descriptions.
4. Define required and optional properties.
5. Define identity and session behavior.
6. Review sensitive-data exposure.
7. Define validation and ownership.
8. Plan versioning for breaking changes.

## Output

- Event catalog
- Property dictionary
- Identity rules
- Privacy constraints
- Owners
- Validation plan

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
