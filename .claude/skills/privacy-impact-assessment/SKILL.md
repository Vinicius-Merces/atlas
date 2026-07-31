---
name: privacy-impact-assessment
description: "Identify privacy risks created by a feature, integration, or data flow."
---

# Privacy Impact Assessment Skill

## Purpose

Identify privacy risks created by a feature, integration, or data flow.

## Inputs

- Data categories
- Processing purpose
- Users and subjects
- Retention
- Sharing
- Jurisdictions or policy scope

## Procedure

1. Map collection and sources.
2. Confirm purpose and necessity.
3. Minimize fields and access.
4. Review retention and deletion.
5. Review consent and user controls.
6. Review third-party sharing.
7. Identify high-risk processing.
8. Define mitigations and evidence.

## Output

- Data map
- Purpose
- Risks
- Required controls
- Residual risk
- Review outcome

## Domain

The skill covers the project and engineering context described by its purpose: Identify privacy risks created by a feature, integration, or data flow.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Identify privacy risks created by a feature, integration, or data flow.
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
