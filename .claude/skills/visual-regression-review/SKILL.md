---
name: visual-regression-review
description: "Create and review deterministic browser screenshots when frontend changes need evidence against clipping, overflow, spacing, typography, crop, and layout regressions."
---

# Visual Regression Review Skill

## Purpose

Turn visual QA into reproducible evidence rather than subjective memory. Use browser screenshots and stable comparison conditions to detect layout regressions that unit tests, type checks, and build success cannot see.

## Inputs

- Routes or states under review
- Baseline screenshots when available
- Supported viewport matrix
- Fonts, media, fixtures, and deterministic test data
- Existing Playwright or browser-test infrastructure
- Visual direction and acceptance criteria

## Procedure

1. Identify critical routes, interaction states, breakpoints, and content variants.
2. Stabilize test data, fonts, time-dependent content, animations, carousels, random values, and network responses as much as the project allows.
3. Capture screenshots at representative viewport sizes and states.
4. Prefer Playwright screenshot assertions such as `toHaveScreenshot` when the repository already supports automated visual comparison.
5. Disable or freeze non-essential animation during deterministic screenshot capture unless the animation state itself is under test.
6. Compare full-page composition and targeted components where local regressions need stronger signal.
7. Inspect differences for overflow, clipping, alignment, spacing rhythm, typography, crop/focal point, stacking context, sticky/fixed collisions, and unintended color/surface changes.
8. Treat baseline updates as code changes that require explanation; never update snapshots merely to make CI green.
9. Store or reference evidence according to repository policy without committing unnecessary binary churn when the project uses an external artifact strategy.
10. Re-run after corrections and record final status.

## Required visual states

Where applicable, include:

- default/load-complete state
- loading/skeleton state
- empty/error state
- navigation open/closed
- form focus/error/success
- hover/focus/touch-relevant alternatives where deterministic
- long copy or localization stress state
- small phone, common phone, tablet/laptop, desktop, and large desktop compositions
- reduced-motion or motion-disabled capture for stable structural review

## Anti-vibe-code requirements

Visual regression is not only about preserving pixels. Review whether a change accidentally introduces generic visual defaults, repeated card formulas, excessive radii/glow, weak hierarchy, or inconsistent spacing even when those pixels are technically new rather than regressed.

## Output

- Routes/states/viewports captured
- Baseline source and determinism notes
- Screenshot or artifact references
- Findings with severity
- Baseline changes requiring approval
- Retest status

## Trigger conditions

Use after meaningful frontend visual changes, before frontend release, after responsive fixes, after motion/3D integration, or when users report that a page looks broken at particular sizes.

## Dependencies

- `responsive-layout-audit`
- `frontend-craft-review`
- `test-strategy-design`
- Existing browser automation or equivalent reproducible capture capability

## Limitations

- Pixel comparison cannot judge product intent by itself.
- Screenshot stability depends on deterministic fixtures and rendering environment.
- Does not replace accessibility or interaction testing.

## Validation

- Capture at the declared viewport/state matrix.
- Explain every accepted baseline change.
- Confirm animations and nondeterministic data cannot create false diffs.
- Confirm critical layout findings are resolved or explicitly block release.
