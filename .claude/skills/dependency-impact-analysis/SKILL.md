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

## Domain

The skill covers the project and engineering context described by its purpose: Evaluate the risk and value of adding or upgrading a dependency.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Evaluate the risk and value of adding or upgrading a dependency.
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
