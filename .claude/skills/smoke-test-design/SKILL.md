---
name: smoke-test-design
description: "Create fast checks that verify critical framework and adapter behavior."
---

# Smoke-Test Design Skill

## Purpose

Create fast checks that verify critical framework and adapter behavior.

## Procedure

1. Identify release-critical paths.
2. Select minimal representative scenarios.
3. Keep tests deterministic.
4. Validate structure, registry, commands, and adapters.
5. Produce actionable failures.
6. Run locally and in CI.
7. Document coverage and limitations.

## Output

- Smoke-test suite
- Covered paths
- Failure messages
- Known gaps

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to smoke test design.
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
