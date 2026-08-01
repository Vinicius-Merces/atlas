---
name: localization-readiness-assessment
description: "Assess whether a product or feature is structurally ready for translation and locale variation."
---

# Localization Readiness Assessment Skill

## Purpose

Assess whether a product or feature is structurally ready for translation and
locale variation.

## Checks

- Externalized strings
- Message context
- Pluralization
- Gender and grammatical variants
- Text expansion
- Bidirectional layouts
- Locale formatting
- Sort and search behavior
- Fonts and glyph support
- Translation fallback
- Image and cultural assumptions

## Output

- Readiness level
- Blocking issues
- Engineering changes
- Content changes
- QA requirements

## Trigger conditions

- Trigger within declared scope when required evidence is available, or record its absence as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to localization readiness assessment.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository/runtime inspection and validation capabilities the procedure requires.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.
