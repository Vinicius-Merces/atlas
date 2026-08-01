---
name: version-migration-planning
description: "Plan migration between ATLAS versions or compatible runtime adapter versions."
---

# Version Migration Planning Skill

## Purpose

Plan migration between ATLAS versions or compatible runtime adapter versions.

## Procedure

1. Identify source and target versions.
2. Compare registry, paths, contracts, and runtime metadata.
3. Identify additive, transitional, and breaking changes.
4. Map affected project customizations.
5. Define backup and rollback.
6. Sequence file replacement and manual edits.
7. Run validation.
8. Record completed migration and remaining exceptions.

## Output

- Version delta
- Breaking changes
- Migration steps
- Backup plan
- Validation
- Rollback
- Completion report

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to version migration planning.
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
