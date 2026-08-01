---
name: dependency-impact-analysis
description: "Evaluate the risk and value of adding or upgrading a dependency."
---

# Dependency Impact Analysis Skill

## Purpose

Evaluate the risk and value of adding or upgrading a dependency.

## Inputs

- Dependency name and version
- Current version
- Release notes
- Known consumers
- Runtime constraints

## Procedure

1. Identify direct and transitive impact.
2. Review breaking changes and deprecations.
3. Check security and maintenance status.
4. Check runtime and platform compatibility.
5. Assess bundle, image, or build impact.
6. Define targeted tests.
7. Define rollback.

## Output

- Upgrade recommendation
- Breaking changes
- Security findings
- Validation plan
- Rollback path

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
