---
name: web-performance-field-readiness
description: "Assess user-facing performance before release when images, fonts, animation, WebGL, third-party scripts, or client JavaScript could threaten real-device experience."
---

# Web Performance Field Readiness Skill

## Purpose

Validate that a visually ambitious frontend remains fast, responsive, stable, and usable on realistic devices and networks. Treat performance as part of the design rather than as a cleanup step after visual implementation.

## Inputs

- Implemented frontend and build output
- Performance budgets and user/device assumptions
- Images, video, fonts, 3D assets, and third-party scripts
- Motion/GSAP/Motion/R3F usage
- Route and hydration architecture
- Existing lab and field telemetry when available

## Procedure

1. Inventory the critical rendering path, client bundles, images, fonts, video, WebGL assets, third-party scripts, and persistent animation loops.
2. Identify the primary user-visible milestones: initial content, hero/media readiness, primary interaction readiness, and route transitions.
3. Validate image dimensions, formats, responsive sources, lazy/eager policy, focal crop, and loading priority.
4. Validate font subset/weight strategy, fallback behavior, preload policy, and layout-shift risk.
5. Measure or inspect JavaScript shipped to the client, hydration cost, duplicated libraries, and avoidable client boundaries.
6. Review GSAP/Motion behavior for excessive observers, unmanaged timelines, layout-triggering animation, and continuous work when idle.
7. Review R3F/Three.js for DPR, draw calls, texture/model cost, post-processing, frameloop policy, adaptive quality, and mobile fallback.
8. Review scroll-linked effects for main-thread contention and jank on representative devices.
9. Verify loading/error/fallback states prevent blank or unusable experiences while heavy media initializes.
10. Compare lab evidence with field telemetry when available; do not claim field readiness from a single desktop Lighthouse run alone.
11. Record regressions against the project's performance budget and require remediation or explicit acceptance.

## Performance design rules

- Do not trade core usability for decorative effects.
- Do not preload every premium asset.
- Do not keep WebGL or animation loops running when the experience can be idle.
- Do not ship both GSAP and Motion for overlapping responsibilities without justification.
- Do not use desktop-only media/3D quality unchanged on weak mobile devices.
- Do not solve poor perceived performance with longer skeletons or loaders when the underlying cost can be removed.

## Output

- Critical-path inventory
- Asset and JavaScript risk findings
- Motion/3D runtime findings
- Loading and perceived-performance findings
- Budget comparison
- Mobile/weak-device adaptations
- Field/lab evidence distinction
- Release blockers and residual risk

## Trigger conditions

Use before release when the frontend adds or materially changes animation, 3D/WebGL, large media, custom fonts, third-party scripts, client-heavy components, or other work that can affect user-perceived speed and responsiveness.

## Dependencies

- `performance-budget-analysis`
- `frontend-stack-selection`
- `motion-choreography` when animation exists
- `immersive-3d-experience` when WebGL exists
- `responsive-layout-audit`

## Limitations

- Does not invent field telemetry when none exists.
- Does not reduce all performance assessment to one synthetic score.
- Does not require removal of intentional visual richness when evidence shows the budget remains healthy.

## Validation

- Record measured or directly inspected evidence, not impressions alone.
- Test at least one constrained mobile/network profile when visual features are non-trivial.
- Verify idle CPU/GPU behavior for persistent animation/3D surfaces where applicable.
- Verify loading, error, and fallback states.
- Distinguish lab measurements from real-user/field evidence in the final result.
