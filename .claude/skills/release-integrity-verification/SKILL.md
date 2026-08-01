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

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to release integrity verification.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.
