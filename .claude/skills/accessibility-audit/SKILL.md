---
name: accessibility-audit
description: "Review user-facing work for common accessibility failures."
---

# Accessibility Audit Skill

## Purpose

Review user-facing websites and application interfaces for accessibility barriers that can prevent people from perceiving, understanding, navigating, or operating the experience. Use the project's stated accessibility target when one exists; otherwise use WCAG 2.2 Level AA as the default review baseline and record any criteria that require specialized assistive-technology or user testing.

The audit treats accessibility as a product and engineering requirement, not as a final automated scan. Prefer native HTML semantics where they satisfy the interaction. When ARIA is necessary, verify the matching keyboard behavior, state management, focus handling, names, descriptions, and announcements.

## Trigger conditions

Use this skill when reviewing or changing a user-facing page, component, navigation system, form, modal, menu, data table, interactive visualization, rich widget, checkout, onboarding flow, or other experience where accessibility can regress.

Trigger it before calling significant frontend work release-ready, after introducing a new interaction pattern, when changing focus or keyboard behavior, after a design-system primitive changes, or when browser/user evidence reports an accessibility failure.

For purely non-visual backend changes with no user-interface or generated-content impact, do not force this audit unless the acceptance criteria require it.

## Inputs

- Task envelope with scope, acceptance criteria, risk, target browsers/devices, and applicable accessibility standard.
- Rendered interface or reproducible browser route, not only source code or design mockups.
- Relevant component source, design-system primitives, styles, content, validation rules, and interaction state.
- Representative viewport sizes, zoom/reflow conditions, loading/error/empty/disabled states, and localization or long-content cases when applicable.
- Existing automated accessibility results, browser diagnostics, user reports, or prior audit evidence when available.
- Known product constraints involving animation, WebGL/canvas, audio/video, charts, custom widgets, authentication, checkout, or other critical journeys.

## Procedure

1. **Establish scope and baseline.** Identify affected journeys, components, accessibility target, supported input modes, and evidence that can be collected. Do not claim conformance for surfaces that were not inspected.
2. **Inspect semantic structure.** Check document language, landmarks, heading hierarchy, meaningful element choice, lists/tables, accessible names and descriptions, image alternatives, labels, and relationships. Prefer native controls over recreating their semantics with generic elements.
3. **Exercise keyboard operation.** Navigate with keyboard only. Verify every operable control is reachable and usable, focus order follows task meaning, focus is visible and not obscured, composite widgets use an appropriate keyboard model, and opening/closing overlays restores focus predictably.
4. **Review forms and validation.** Confirm programmatic labels, instructions, required/invalid state, autocomplete where relevant, field grouping, error association, summary/focus behavior, and recovery. Errors must not depend on color alone.
5. **Check visual accessibility.** Inspect text and non-text contrast where applicable, text resizing, responsive reflow, zoom, truncation, content overlap, target sizing, orientation assumptions, spacing overrides, and whether information survives user style changes when relevant.
6. **Check motion and media.** Respect reduced-motion preferences and avoid essential information being conveyed only through movement. Verify pause/stop controls and captions/transcripts or alternatives when applicable time-based media exists.
7. **Inspect dynamic behavior.** Verify loading, async completion, validation, toasts, dialogs, route changes, expanding regions, live updates, and other state changes expose appropriate semantics and announcements without excessive or duplicate live-region noise.
8. **Inspect custom widgets and rich surfaces.** For ARIA widgets, verify role/state/property use together with expected focus and keyboard behavior. For canvas/WebGL/charts, require an accessible DOM alternative or equivalent information/action path rather than assuming visual rendering is sufficient.
9. **Run automation as supporting evidence.** Use project-native linting, accessibility rules, browser checks, or scanners where available. Treat a clean automated scan as partial evidence only because it cannot prove keyboard usability, meaningful alternatives, reading order, cognitive clarity, or real assistive-technology behavior.
10. **Classify and remediate.** Record the barrier, affected users/journey, severity, evidence, relevant criterion or pattern when known, remediation, owner, and verification method. Re-test the corrected interaction rather than accepting the code change alone.

## Outputs

- Audit scope and accessibility target.
- Findings grouped by Critical, High, Medium, Low, or Note severity.
- For each finding: affected route/component, user impact, reproducible evidence, remediation, and verification method.
- Keyboard and focus test result for material interactive journeys.
- Automated-tool result when available, clearly separated from manual evidence.
- Residual validation gaps requiring screen-reader, switch, voice-control, magnification, cognitive/usability, or real-user testing.
- Final outcome: Approved, Approved with conditions, Changes required, or Blocked.

## Dependencies

- Canonical ATLAS contracts, project memory, and the closest mapped frontend or feature-delivery workflow.
- `browser-flow-validation` when critical accessibility behavior must be demonstrated in a rendered journey.
- `responsive-layout-audit` for reflow, viewport, zoom, clipping, and responsive composition evidence.
- `motion-choreography` or `frontend-craft-review` when motion or premium interaction design is materially involved.
- Repository/runtime inspection plus project-native tests and browser tooling required to reproduce the interaction.

## Limitations

This skill does not establish legal compliance and does not replace evaluation by disabled users or specialists using real assistive technologies. Automated tools detect only a subset of accessibility failures, and browser/DOM inspection cannot prove that wording, alternative text, interaction efficiency, or cognitive load is appropriate for every user.

If required evidence cannot be obtained, mark the affected claim as unverified rather than assuming the absence of an error means accessibility. A Critical or High barrier in a required journey blocks accessibility approval until corrected or explicitly accepted by the product's authorized risk owner.

## Validation

- Exercise the material journey with keyboard only and confirm operability, logical focus order, visible focus, overlay focus containment/restoration, and no keyboard trap.
- Inspect the accessibility tree or equivalent browser semantics for names, roles, states, relationships, landmarks, headings, and dynamic announcements on representative components.
- Verify form labels, descriptions, invalid/error association, recovery behavior, and server/client error states rather than only the happy path.
- Test representative phone, tablet, and desktop layouts plus browser zoom/reflow where applicable; confirm content and controls remain available without harmful clipping or overlap.
- Check reduced-motion behavior when animation, parallax, scrolling choreography, video, or WebGL is present.
- Run available automated accessibility checks and inspect every reported violation; do not suppress rules merely to obtain a green result.
- Reproduce at least one negative or edge state for each material custom interaction, such as empty/error/loading/disabled/expanded/dialog-open states.
- Re-test remediated findings in the rendered interface and preserve screenshots, browser traces, test output, or concise manual evidence sufficient for independent review.
