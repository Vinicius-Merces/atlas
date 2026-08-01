---
name: command-catalog-synthesis
description: "Produce a runtime-oriented catalog of all canonical ATLAS commands."
---

# Command Catalog Synthesis Skill

## Purpose

Produce a runtime-oriented catalog of all canonical ATLAS commands.

## Procedure

1. Read command names from the registry.
2. Resolve canonical command files.
3. Extract purpose where available.
4. Generate runtime catalog entries.
5. Mark unsupported invocation differences.
6. Validate completeness.

## Output

- Command catalog
- Missing commands
- Invocation notes
- Validation status

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to command catalog synthesis.
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
