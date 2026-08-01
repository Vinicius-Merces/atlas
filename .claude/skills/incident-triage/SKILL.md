---
name: incident-triage
description: "Rapidly classify and stabilize a production incident."
---

# Incident Triage Skill

## Purpose

Rapidly classify and stabilize a production incident.

## Inputs

- Symptoms
- User impact
- Start time
- Recent changes
- Available telemetry

## Procedure

1. Confirm impact and severity.
2. Establish incident ownership.
3. Preserve evidence.
4. Identify recent changes.
5. Form and test containment hypotheses.
6. Mitigate or roll back.
7. Communicate current status.
8. Transition to recovery and analysis.

## Output

- Severity
- Impact
- Current hypothesis
- Mitigation
- Next validation
- Communication status

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
