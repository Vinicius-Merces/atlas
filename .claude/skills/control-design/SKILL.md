---
name: control-design
description: "Design a proportionate preventive, detective, or corrective control."
---

# Control Design Skill

## Purpose

Design a proportionate preventive, detective, or corrective control.

## Inputs

- Risk or requirement
- System scope
- Existing workflow
- Evidence expectations

## Procedure

1. Define the risk and desired outcome.
2. Select preventive, detective, corrective, or compensating control.
3. Define owner and enforcement point.
4. Define evidence and failure behavior.
5. Define exceptions.
6. Define testing and review cadence.
7. Define effectiveness metrics.
8. Minimize unnecessary delivery friction.

## Output

- Control objective
- Control design
- Owner
- Evidence
- Exception process
- Review cadence
- Effectiveness metric

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
