---
name: component-reuse-assessment
description: "Determine whether an existing frontend component should be reused, extended, or replaced."
---

# Component Reuse Assessment Skill

## Purpose

Determine whether an existing frontend component should be reused, extended, or
replaced.

## Inputs

- Requested UI behavior
- Existing components
- Design system constraints
- Accessibility requirements

## Procedure

1. Search for related components.
2. Compare semantic purpose.
3. Compare API and state needs.
4. Check styling and accessibility compatibility.
5. Estimate extension complexity.
6. Detect duplication risk.
7. Recommend reuse, composition, extension, or new component.

## Output

- Candidate components
- Compatibility findings
- Risks
- Recommendation

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
