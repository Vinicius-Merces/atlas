---
name: registry-to-runtime-generation
description: "Generate runtime catalogs and indexes from the canonical ATLAS registry."
---

# Registry-to-Runtime Generation Skill

## Purpose

Generate runtime catalogs and indexes from the canonical ATLAS registry.

## Procedure

1. Read the registry.
2. Validate collection types.
3. Generate one catalog entry per canonical asset.
4. Preserve canonical names.
5. Link to canonical files when resolvable.
6. Mark generated outputs.
7. Compare generated output with committed files.
8. Report differences.

## Output

- Runtime catalogs
- Generated indexes
- Missing canonical files
- Synchronization status

## Domain

The skill covers the project and engineering context described by its purpose: Generate runtime catalogs and indexes from the canonical ATLAS registry.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Generate runtime catalogs and indexes from the canonical ATLAS registry.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to registry to runtime generation.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository or runtime inspection and validation capabilities required by the procedure.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
