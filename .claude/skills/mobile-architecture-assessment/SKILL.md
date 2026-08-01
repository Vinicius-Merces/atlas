---
name: mobile-architecture-assessment
description: "Evaluate mobile architecture for platform fit, maintainability, offline behavior, performance, and release constraints."
---

# Mobile Architecture Assessment Skill

## Purpose

Evaluate mobile architecture for platform fit, maintainability, offline
behavior, performance, and release constraints.

## Checks

- Navigation and lifecycle
- State ownership
- Local persistence
- Network resilience
- Background tasks
- Permissions
- Platform-specific integrations
- Accessibility
- Device compatibility
- App-store requirements

## Output

- Architecture findings
- Platform risks
- Compatibility concerns
- Recommended structure
- Validation plan

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to mobile architecture assessment.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.
