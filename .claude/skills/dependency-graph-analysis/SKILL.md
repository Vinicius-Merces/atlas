---
name: dependency-graph-analysis
description: "Analyze dependency direction, cycles, coupling, and change impact."
---

# Dependency Graph Analysis Skill

## Purpose

Analyze dependency direction, cycles, coupling, and change impact.

## Inputs

- Repository structure
- Package manifests
- Import graph
- Build configuration

## Procedure

1. Map direct dependencies.
2. Identify shared and foundational packages.
3. Detect cycles.
4. Identify forbidden dependency directions.
5. Estimate affected packages.
6. Identify high-coupling nodes.
7. Recommend boundary improvements.

## Output

- Dependency graph summary
- Cycles
- High-risk coupling
- Affected-change implications
- Recommendations

## Domain

The skill covers the project and engineering context described by its purpose: Analyze dependency direction, cycles, coupling, and change impact.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Analyze dependency direction, cycles, coupling, and change impact.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository or runtime inspection and validation capabilities required by the procedure.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.

## Validation

- Confirm every reported output is traceable to an input, decision, or observed artifact.
- Run applicable contract, schema, runtime, or repository checks named by the task and report failures and residual risk.
