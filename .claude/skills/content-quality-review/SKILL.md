---
name: content-quality-review
description: "Review product copy for clarity, consistency, actionability, and audience fit."
---

# Content Quality Review Skill

## Purpose

Review product copy for clarity, consistency, actionability, and audience fit.

## Checks

- User goal is clear
- Labels match actions
- Errors explain recovery
- Empty states guide the next step
- Terminology is consistent
- Tone fits the context
- Sentences are concise
- Copy avoids unsupported claims
- Content is localization-ready
- Accessibility labels are meaningful

## Output

- Findings
- Severity
- Suggested revisions
- Terminology issues
- Localization risks

## Domain

The skill covers the project and engineering context described by its purpose: Review product copy for clarity, consistency, actionability, and audience fit.

## Trigger conditions

- Use when an assigned task requires the stated outcome: Review product copy for clarity, consistency, actionability, and audience fit.
- Trigger only within declared scope and when required evidence is available or its absence can be recorded as a blocker.

## Inputs

- Task envelope with scope, acceptance criteria, risk, and relevant constraints.
- Current canonical project artifacts and observed evidence relevant to content quality review.
- Any prior decisions, consumer constraints, or runtime context required by the procedure.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped workflow.
- Repository or runtime inspection and validation capabilities required by the procedure.

## Limitations

- Does not grant authority to change assets, waive review gates, approve its own output, or expand task scope.
- Conclusions are limited to supplied and observed evidence; missing or stale evidence must be reported, not guessed.
