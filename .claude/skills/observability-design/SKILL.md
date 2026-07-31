---
name: observability-design
description: "Design logs, metrics, traces, dashboards, and alerts for a feature or service."
---

# Observability Design Skill

## Purpose

Design logs, metrics, traces, dashboards, and alerts for a feature or service.

## Inputs

- System boundaries
- Critical user journeys
- Failure modes
- Operational ownership

## Procedure

1. Identify critical outcomes.
2. Map failure points and dependencies.
3. Define logs, metrics, traces, and events.
4. Add correlation requirements.
5. Define dashboards and alert thresholds.
6. Assign alert ownership.
7. Validate privacy and signal usefulness.

## Output

- Signal map
- Dashboard requirements
- Alerts
- Ownership
- Privacy constraints
- Validation plan

## Domain

The skill covers the project and engineering context described by its purpose: Design logs, metrics, traces, dashboards, and alerts for a feature or service.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Design logs, metrics, traces, dashboards, and alerts for a feature or service.
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
