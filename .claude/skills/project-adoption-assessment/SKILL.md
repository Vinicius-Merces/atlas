---
name: project-adoption-assessment
description: "Determine which ATLAS capabilities should be introduced into a project."
---

# Project Adoption Assessment Skill

## Purpose

Determine which ATLAS capabilities should be introduced into a project.

## Procedure

1. Map repository and architecture.
2. Identify delivery pain points.
3. Assess team and project maturity.
4. Identify current documentation and governance.
5. Identify high-risk gaps.
6. Select minimum useful ATLAS components.
7. Sequence adoption phases.
8. Define success metrics.

## Output

- Current state
- Recommended components
- Adoption phases
- Risks
- Effort
- Success metrics

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to project adoption assessment.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
