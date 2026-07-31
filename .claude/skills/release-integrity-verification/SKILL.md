---
name: release-integrity-verification
description: "Verify that a release artifact is complete, consistent, and traceable."
---

# Release Integrity Verification Skill

## Purpose

Verify that a release artifact is complete, consistent, and traceable.

## Checks

- Version consistency
- Changelog entry
- Registry validity
- Required files
- Adapter inclusion
- Manifest completeness
- Archive integrity
- Checksums
- Validation evidence
- Known limitations

## Output

- Integrity result
- Blocking failures
- Warnings
- Artifact metadata
- Release recommendation

## Domain

The skill covers the project and engineering context described by its purpose: Verify that a release artifact is complete, consistent, and traceable.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Verify that a release artifact is complete, consistent, and traceable.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to release integrity verification.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository or runtime inspection and validation capabilities required by the procedure.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.
