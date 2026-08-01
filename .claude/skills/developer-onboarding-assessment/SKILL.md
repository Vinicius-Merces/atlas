---
name: developer-onboarding-assessment
description: "Evaluate whether a new contributor can understand, run, test, and modify the project reliably."
---

# Developer Onboarding Assessment Skill

## Purpose

Evaluate whether a new contributor can understand, run, test, and modify the
project reliably.

## Procedure

1. Inspect prerequisites.
2. Follow setup from a clean environment.
3. Verify local commands.
4. Verify environment configuration.
5. Verify tests and linting.
6. Inspect error messages.
7. Inspect architecture discoverability.
8. Record friction and missing documentation.

## Output

- Setup success
- Time-to-first-run factors
- Blocking friction
- Documentation gaps
- Tooling recommendations

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to developer onboarding assessment.
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
