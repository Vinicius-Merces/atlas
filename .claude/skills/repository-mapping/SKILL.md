---
name: repository-mapping
description: "Create a reliable structural map of an unfamiliar repository."
---

# Repository Mapping Skill

## Purpose

Create a reliable structural map of an unfamiliar repository.

## Procedure

1. Identify repository type and package manager.
2. Locate entry points and applications.
3. Identify packages, services, and libraries.
4. Identify configuration and build systems.
5. Map test locations.
6. Map data and integration boundaries.
7. Identify ownership signals.
8. Identify risky or generated areas.

## Output

- Repository summary
- Directory map
- Applications and packages
- Build and test commands
- Architecture signals
- Unknowns and risks

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to repository mapping.
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
