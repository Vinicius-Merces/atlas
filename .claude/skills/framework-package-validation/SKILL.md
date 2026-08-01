---
name: framework-package-validation
description: "Verify that an ATLAS distribution is structurally complete and internally consistent."
---

# Framework Package Validation Skill

## Purpose

Verify that an ATLAS distribution is structurally complete and internally
consistent.

## Procedure

1. Read `VERSION`.
2. Compare version references in README, registry, and runtime metadata.
3. Validate required directories.
4. Validate registry JSON.
5. Validate agent metadata.
6. Confirm referenced files exist.
7. Confirm changelog contains the current version.
8. Detect empty placeholders and broken links where possible.
9. Verify archive readability.
10. Produce validation report.

## Output

- Package version
- File count
- Passed checks
- Failed checks
- Warnings
- Release recommendation

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to framework package validation.
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
