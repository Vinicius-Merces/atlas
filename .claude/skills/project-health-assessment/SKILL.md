---
name: project-health-assessment
description: Assess a project's technical and operational health using consistent evidence.
---

# Project Health Assessment Skill

## Purpose

Assess a project's technical and operational health using consistent evidence.

## Procedure

1. Define project scope.
2. Map product, architecture, repository, delivery, and operations.
3. Inspect tests, CI, releases, security, and observability.
4. Inspect memory, ADRs, ownership, and documentation.
5. Assess cost and maintenance signals.
6. Rate each health dimension.
7. Record unknowns and missing evidence.
8. Prioritize improvements.

## Output

- Health scorecard
- Evidence
- Risks
- Unknowns
- Improvement priorities
- Review cadence

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to project health assessment.
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
