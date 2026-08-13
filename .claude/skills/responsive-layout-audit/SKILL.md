---
name: responsive-layout-audit
description: "Audit responsive composition across viewport and container sizes when user-facing layouts must remain intentional rather than merely stacking on smaller screens."
---

# Responsive Layout Audit Skill

## Purpose

Verify that a frontend preserves hierarchy, readability, interaction quality, media composition, and visual intent across real viewport and container constraints.

Responsive quality is not satisfied by making content technically fit. The composition must still feel designed at each size.

## Inputs

- Implemented frontend or prototype
- Supported viewport/device requirements
- Design tokens and layout primitives
- Media assets and crop rules
- Interaction and motion behavior
- Known browser constraints

## Required coverage

At minimum, test representative widths spanning:

- small phone around 320 px
- common phone around 375-390 px
- large phone/small tablet around 430-768 px
- tablet/small laptop around 768-1024 px
- common laptop around 1280-1440 px
- large desktop around 1600-1920 px

Use project-specific breakpoints when they are more authoritative. Test height constraints too, especially around common laptop heights where large heroes, sticky sections, and modals often fail.

## Procedure

1. Inspect layout primitives, breakpoints, container queries, min/max widths, fluid type, and media queries.
2. Render the page at representative widths and heights instead of resizing by intuition only.
3. Check horizontal overflow, accidental clipping, fixed-width assumptions, viewport-unit traps, sticky/fixed collisions, and safe-area behavior.
4. Verify typography: line length, wrapping, widows/orphans where material, heading scale, button labels, and long localized strings where applicable.
5. Verify media: crop, focal point, aspect ratio, object positioning, loading placeholders, and art direction.
6. Verify spacing rhythm and section proportions, not only individual component fit.
7. Verify grids recombine intentionally; do not accept desktop card grids converted mechanically to a long undifferentiated vertical stack when hierarchy can be preserved better.
8. Verify navigation, menus, dialogs, forms, tables, carousels, tooltips, and dense product controls at touch sizes.
9. Verify motion and scroll choreography at each relevant class of viewport; disable or redesign effects that become awkward, expensive, or obstructive on small screens.
10. Verify R3F/WebGL canvas sizing, fallback, DPR policy, and overlap with DOM content when present.
11. Re-check large screens for over-stretched lines, oversized empty zones, weak anchoring, and lost focal hierarchy.

## Anti-vibe-code requirements

- Do not treat `flex-direction: column` as a complete mobile design strategy.
- Do not hide important content on mobile merely to avoid layout work.
- Do not preserve cinematic desktop effects when they damage mobile comprehension or performance.
- Do not allow every section to become the same full-width card stack.
- Do not fix one target phone while leaving intermediate widths broken.

## Output

- Viewports and containers tested
- Findings with severity and screenshots/evidence where available
- Overflow/crop/typography/spacing findings
- Interaction and motion findings
- Large-screen findings
- Required corrections and retest status

## Trigger conditions

Use for any meaningful user-facing layout change, especially marketing pages, dashboards, responsive navigation, hero redesigns, media-heavy sections, sticky/scroll experiences, or before release of a frontend with visual changes.

## Dependencies

- `interface-visual-direction`
- `motion-choreography` when animation exists
- `immersive-3d-experience` when WebGL exists
- `visual-regression-review`
- `accessibility-audit`

## Limitations

- Viewport coverage is representative, not a substitute for project-specific analytics or device requirements.
- Does not approve visual craft independently.

## Validation

- No unexplained horizontal overflow at supported widths.
- No clipped actionable content.
- Typography remains readable and intentional.
- Key media retains intended focal content.
- Navigation and primary tasks remain usable by touch and keyboard.
- Responsive motion/3D behavior is explicitly validated rather than assumed from desktop.
