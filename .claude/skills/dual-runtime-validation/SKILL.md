---
name: dual-runtime-validation
description: "Validate Claude Code and Codex runtime support in the same release."
---

# Dual-Runtime Validation Skill

## Purpose

Validate Claude Code and Codex runtime support in the same release.

## Procedure

1. Validate canonical registry.
2. Validate Claude Code runtime metadata.
3. Validate Codex manifest.
4. Compare mapped collections.
5. Run contract tests.
6. Run Codex-specific tests.
7. Review unsupported features.
8. Produce support recommendation.

## Output

- Claude validation
- Codex validation
- Parity status
- Gaps
- Release recommendation

## Domain

The skill covers the project and engineering context described by its purpose: Validate Claude Code and Codex runtime support in the same release.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Validate Claude Code and Codex runtime support in the same release.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to dual runtime validation.
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
