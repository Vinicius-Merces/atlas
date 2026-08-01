---
name: accessibility-audit
description: "Review user-facing work for common accessibility failures."
---

# Accessibility Audit Skill

## Purpose

Review user-facing work for common accessibility failures.

## Checks

- Semantic structure
- Heading hierarchy
- Keyboard navigation
- Focus visibility
- Labels and descriptions
- Form error association
- Color contrast
- Motion preferences
- Screen-reader announcements
- Touch target size
- Responsive zoom behavior

## Output

- Findings
- Severity
- User impact
- Recommended remediation
- Validation gaps

## Limitation

This skill supports review but does not replace testing with assistive
technologies and real users.

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to accessibility audit.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.
