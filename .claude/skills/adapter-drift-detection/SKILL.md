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

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to adapter drift detection.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.
