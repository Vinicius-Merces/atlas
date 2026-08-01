---
name: runtime-adapter-mapping
description: "Map canonical ATLAS capabilities to a target AI coding runtime."
---

# Runtime Adapter Mapping Skill

## Purpose

Map canonical ATLAS capabilities to a target AI coding runtime.

## Procedure

1. Inventory target runtime capabilities.
2. Map agents, skills, commands, workflows, and tools.
3. Identify unsupported or partial features.
4. Define target directory structure.
5. Define syntax translation.
6. Preserve semantic contracts.
7. Define validation scenarios.
8. Produce compatibility notes.

## Output

- Capability matrix
- Adapter structure
- Translation rules
- Unsupported features
- Validation plan

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to runtime adapter mapping.
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
