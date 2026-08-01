---
name: codex-runtime-generation
description: "Generate or synchronize the Codex adapter from canonical ATLAS definitions."
---

# Codex Runtime Generation Skill

## Purpose

Generate or synchronize the Codex adapter from canonical ATLAS definitions.

## Procedure

1. Read canonical registry.
2. Map agents to Codex role instructions.
3. Map commands to Codex task entry points.
4. Map workflows to execution procedures.
5. Map reviews to verification passes.
6. Preserve memory and contract references.
7. Generate runtime manifest.
8. Validate required assets.
9. Run Codex compatibility tests.

## Output

- Generated Codex adapter
- Capability matrix
- Unsupported features
- Validation results

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to codex runtime generation.
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
