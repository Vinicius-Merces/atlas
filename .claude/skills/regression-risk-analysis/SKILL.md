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
