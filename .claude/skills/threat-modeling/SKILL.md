---
name: threat-modeling
description: "Identify threats and controls for a system, feature, integration, or data flow."
---

# Threat Modeling Skill

## Purpose

Identify threats and controls for a system, feature, integration, or data flow.

## Procedure

1. Define scope and assumptions.
2. Identify assets and sensitive data.
3. Draw data flows and trust boundaries.
4. Identify actors and entry points.
5. Enumerate threats and abuse cases.
6. Evaluate existing controls.
7. Prioritize by likelihood and impact.
8. Define mitigations and residual risk.
9. Define review triggers.

## Output

- Scope
- Data-flow summary
- Assets
- Trust boundaries
- Threat register
- Controls
- Required mitigations
- Residual risk

## Domain

The skill covers the project and engineering context described by its purpose: Identify threats and controls for a system, feature, integration, or data flow.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Identify threats and controls for a system, feature, integration, or data flow.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to threat modeling.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository or runtime inspection and validation capabilities required by the procedure.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
