---
name: motion-choreography
description: "Design and implement purposeful UI motion when a frontend needs transitions, gestures, scroll choreography, or timelines, selecting CSS, Motion, or GSAP by interaction semantics."
---

# Motion Choreography Skill

## Purpose

Create a coherent motion language that explains state, reinforces hierarchy, supports spatial continuity, and adds brand character without turning animation into decoration.

## Tool selection

- Use CSS transitions/keyframes for simple local effects with no sequencing or shared state.
- Use Motion for React-owned gestures, enter/exit states, layout changes, shared-layout transitions, springs, drag, hover/tap/focus, and component-scoped animation.
- Use GSAP for coordinated timelines, multi-element sequencing, complex transforms, ScrollTrigger narratives, pin/scrub/snap behavior, and imperative animation spanning multiple DOM regions.
- Do not use two animation systems for the same responsibility without an explicit interoperability reason.

## Inputs

- Visual direction and interaction intent
- Existing animation libraries and patterns
- Component architecture
- Scroll/story requirements
- Performance targets and supported devices
- Accessibility and reduced-motion requirements

## Procedure

1. Inventory every proposed animated behavior and state transition.
2. Assign each behavior a purpose: orientation, feedback, continuity, emphasis, narrative, delight, or spatial explanation.
3. Remove animation that has no user or brand value.
4. Select CSS, Motion, or GSAP according to the ownership and sequencing rules above.
5. Define timing ranges, easing/spring character, staggering policy, transform origins, and interruption behavior.
6. For scroll-linked animation, define start/end conditions, pinning, scrub semantics, mobile behavior, and content accessibility without animation.
7. For GSAP in React, scope selectors and ensure lifecycle cleanup; use the project-approved React integration pattern rather than unmanaged global selectors.
8. For Motion, prefer component-scoped gestures/layout semantics and honor reduced-motion utilities where applicable.
9. Avoid animating expensive layout properties when transforms/opacity can communicate the same behavior.
10. Validate touch behavior, keyboard/focus behavior, resize/orientation changes, hydration, and route transitions.
11. Implement a reduced-motion path that removes or substantially tones down non-essential movement while preserving meaning.

## Choreography rules

- Motion must vary by semantic role; a modal, navigation transition, editorial reveal, and CTA feedback should not all use the same fade-up recipe.
- Scroll choreography must not trap the user, obscure content, or require precision scrolling.
- Pinned sequences must have a useful non-pinned/mobile composition.
- Repeated animation should become quieter as information density increases.
- Large parallax, scale, rotation, camera movement, and continuous loops require stronger justification because they have accessibility and performance cost.
- Hover-only meaning is invalid; touch and keyboard equivalents must exist where interaction is required.

## Output

- Motion inventory and purpose map
- Tool assignment per behavior
- Timing/easing/spring rules
- Scroll choreography specification
- Reduced-motion behavior
- Mobile/touch adaptations
- Cleanup/lifecycle requirements
- Performance risks and validation evidence

## Trigger conditions

Use when a frontend includes meaningful animation, route transitions, shared-layout transitions, scroll-linked storytelling, GSAP/ScrollTrigger, Motion, parallax, pinned sections, or complex interaction feedback.

## Dependencies

- `framework/frontend-craft-model.md`
- `frontend-stack-selection`
- `interface-visual-direction`
- `performance-budget-analysis`
- `accessibility-audit`

## Limitations

- Does not add animation merely to increase perceived polish.
- Does not override product usability or accessibility for spectacle.
- Does not authorize WebGL/3D; use `immersive-3d-experience` for spatial rendering.

## Validation

- Test with reduced motion enabled.
- Test keyboard, pointer, and touch paths.
- Test representative mobile and desktop viewports.
- Verify no stale timelines/listeners survive unmount or route changes.
- Verify animation preserves content access when scripts fail or are disabled where applicable.
- Record any persistent loops, pinned scroll regions, or high-cost effects as explicit performance risks.
