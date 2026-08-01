---
name: support-classification
description: "Classify a runtime, capability, adapter, workflow, or feature by support level."
---

# Support Classification Skill

## Purpose

Classify a runtime, capability, adapter, workflow, or feature by support level.

## Inputs

- Documentation
- Ownership
- Validation evidence
- Compatibility evidence
- Known limitations
- Maintenance commitment

## Output

- Support state
- Evidence
- Limitations
- Missing requirements
- Transition path

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
