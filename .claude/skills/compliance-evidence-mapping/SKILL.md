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
