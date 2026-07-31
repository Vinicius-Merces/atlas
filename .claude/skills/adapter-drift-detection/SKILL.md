---
name: adapter-drift-detection
description: "Detect divergence between a supported runtime adapter and canonical ATLAS."
---

# Adapter Drift Detection Skill

## Purpose

Detect divergence between a supported runtime adapter and canonical ATLAS.

## Checks

- Version
- Registry inventory
- Canonical paths
- Generated catalogs
- Shared contracts
- Shared memory
- Support claims
- Broken references

## Output

- Drift items
- Drift type
- Severity
- Evidence
- Required remediation

## Domain

The skill covers the project and engineering context described by its purpose: Detect divergence between a supported runtime adapter and canonical ATLAS.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Detect divergence between a supported runtime adapter and canonical ATLAS.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to adapter drift detection.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository or runtime inspection and validation capabilities required by the procedure.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.
