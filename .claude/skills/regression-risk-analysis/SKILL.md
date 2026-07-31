---
name: regression-risk-analysis
description: "Estimate the likelihood and impact of regressions before implementation or release."
---

# Regression Risk Analysis Skill

## Purpose

Estimate the likelihood and impact of regressions before implementation or
release.

## Inputs

- Change scope
- Dependency graph
- Shared components
- Test coverage
- Production criticality

## Risk factors

- Shared code
- Data migration
- Public contract change
- Weak test coverage
- Hidden side effects
- Cross-service dependency
- Authentication or billing impact

## Output

- Risk level
- Affected areas
- Required test depth
- Rollback expectations
- Review requirements

## Domain

The skill covers the project and engineering context described by its purpose: Estimate the likelihood and impact of regressions before implementation or release.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Estimate the likelihood and impact of regressions before implementation or release.
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
