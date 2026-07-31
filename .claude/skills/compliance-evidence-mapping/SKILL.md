---
name: compliance-evidence-mapping
description: "Map requirements to controls, implementation evidence, and ownership."
---

# Compliance Evidence Mapping Skill

## Purpose

Map requirements to controls, implementation evidence, and ownership.

## Inputs

- Requirement set
- System scope
- Existing controls
- Available evidence

## Procedure

1. Normalize requirements.
2. Identify applicable systems and owners.
3. Map each requirement to a control.
4. Link implementation evidence.
5. Identify control and evidence gaps.
6. Assign remediation owners.
7. Record review frequency.

## Output

- Requirement matrix
- Control mapping
- Evidence links
- Gaps
- Owners
- Review cadence

## Domain

The skill covers the project and engineering context described by its purpose: Map requirements to controls, implementation evidence, and ownership.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Map requirements to controls, implementation evidence, and ownership.
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
