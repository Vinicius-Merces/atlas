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
4. Classify each important loading state using the loading-state decision model below instead of applying skeletons/spinners universally.
5. Validate font subset/weight strategy, fallback behavior, preload policy, and layout-shift risk.
6. Measure or inspect JavaScript shipped to the client, hydration cost, duplicated libraries, and avoidable client boundaries.
7. Review GSAP/Motion behavior for excessive observers, unmanaged timelines, layout-triggering animation, and continuous work when idle.
8. Review R3F/Three.js for DPR, draw calls, texture/model cost, post-processing, frameloop policy, adaptive quality, and mobile fallback.
9. Review scroll-linked effects for main-thread contention and jank on representative devices.
10. Verify loading/error/fallback states prevent blank or unusable experiences while heavy media initializes.
11. Compare lab evidence with field telemetry when available; do not claim field readiness from a single desktop Lighthouse run alone.
12. Record regressions against the project's performance budget and require remediation or explicit acceptance.

## Loading-state decision model

Loading UX is adaptive. ATLAS must not require a skeleton, lazy loading, spinner, or progress bar on every element.

### Critical/LCP content

For the primary above-the-fold content and likely Largest Contentful Paint resource:

- do not lazy-load merely because the resource is an image/media asset;
- use eager/high-priority behavior only when measurement and framework semantics justify it;
- reserve dimensions/aspect ratio to avoid layout shift;
- keep the initial meaningful content available without waiting for decorative assets;
- avoid artificial loaders that delay already-renderable content.

### Below-the-fold/deferred content

Use lazy/deferred loading when it reduces initial work without hiding content the user reasonably expects immediately.

Validate:

- intersection/viewport behavior;
- placeholders and reserved geometry when needed;
- error/fallback behavior;
- whether excessive lazy boundaries create request waterfalls or visible pop-in.

### Skeleton

Use a skeleton when:

- the content is genuinely asynchronous;
- its approximate geometry is stable enough to reserve layout;
- displaying a temporary structure helps orientation;
- the wait is long enough that an empty surface would be confusing.

Do not use skeletons to mask unnecessary client fetching, slow bundles, oversized media, or avoidable waterfalls.

### Spinner/indeterminate progress

Use when work has started, duration cannot be estimated meaningfully, and preserving exact content geometry is not useful.

Prefer a local indicator near the action/resource instead of blocking the entire interface when only one region is waiting.

### Determinate progress

Use when the system can report meaningful progress for uploads, exports, imports, generation, processing, migrations, or other multi-step/long-running work.

Do not fabricate percentage progress from timers when the backend has no real progress signal.

### Optimistic/pending state

For user mutations, prefer immediate interaction feedback with explicit pending/success/error states when the operation and rollback semantics support it.

Disable or deduplicate repeat submissions only as required by the mutation contract; do not freeze unrelated interface areas.

### Route/section transitions

Transition motion should explain state continuity and must not extend perceived waiting merely for visual polish. Preserve reduced-motion behavior.

## Performance design rules

- Do not trade core usability for decorative effects.
- Do not preload every premium asset.
- Do not lazy-load likely LCP/critical content by default.
- Do not add skeletons/spinners where content can render immediately.
- Do not keep WebGL or animation loops running when the experience can be idle.
- Do not ship both GSAP and Motion for overlapping responsibilities without justification.
- Do not use desktop-only media/3D quality unchanged on weak mobile devices.
- Do not solve poor perceived performance with longer skeletons or loaders when the underlying cost can be removed.

## Output

- Critical-path inventory
- Asset and JavaScript risk findings
- Motion/3D runtime findings
- Loading-state decision matrix
- Lazy/eager/priority findings
- Loading and perceived-performance findings
- Budget comparison
- Mobile/weak-device adaptations
- Field/lab evidence distinction
- Release blockers and residual risk

## Trigger conditions

Use before release when the frontend adds or materially changes animation, 3D/WebGL, large media, custom fonts, third-party scripts, client-heavy components, loading behavior, or other work that can affect user-perceived speed and responsiveness.

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
- Does not prescribe one universal loading component for all interfaces.

## Validation

- Record measured or directly inspected evidence, not impressions alone.
- Test at least one constrained mobile/network profile when visual features are non-trivial.
- Verify the critical/LCP loading path does not use lazy/deferred behavior without explicit evidence.
- Verify idle CPU/GPU behavior for persistent animation/3D surfaces where applicable.
- Verify loading, pending, error, and fallback states.
- Distinguish lab measurements from real-user/field evidence in the final result.
