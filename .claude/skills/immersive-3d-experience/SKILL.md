---
name: immersive-3d-experience
description: "Design and review web 3D with Three.js or React Three Fiber when spatial interaction or narrative depth is justified, with strict performance, fallback, and accessibility budgets."
---

# Immersive 3D Experience Skill

## Purpose

Use real-time 3D only when it materially improves spatial understanding, product storytelling, interaction, simulation, or brand expression. Prevent WebGL from becoming a decorative tax on performance, battery, accessibility, and maintainability.

## Preferred model

- Use Three.js directly when the project is not React-based or when direct renderer ownership is clearly simpler.
- Prefer React Three Fiber in React applications when scene state, component composition, suspense/loading, and React lifecycle integration benefit the implementation.
- Use Drei helpers selectively for common controls, loaders, abstractions, and adaptive performance when they reduce boilerplate without obscuring critical behavior.
- Keep ordinary DOM content in the DOM when it should remain semantic, selectable, accessible, indexable, or easily responsive.

## Inputs

- Visual direction and spatial narrative
- Existing React/Three.js/R3F architecture
- Target devices and browser support
- Asset inventory: GLTF/GLB, textures, HDRI, video, fonts, shaders
- Performance budget and expected interaction density
- Accessibility and fallback requirements

## Admission test

Before implementation, answer all of the following:

1. What does 3D communicate that a DOM/CSS/2D solution cannot communicate as well?
2. What is the fallback for weak devices, reduced motion, WebGL failure, or constrained data/battery conditions?
3. What is the budget for model size, textures, draw calls, DPR, effects, and continuous rendering?
4. Which content must remain outside the canvas for semantics, SEO, accessibility, or normal browser behavior?

If those answers are weak, do not use 3D.

## Procedure

1. Define scene purpose, camera role, interaction model, and DOM/Canvas boundary.
2. Establish asset budgets before importing production assets.
3. Reuse geometries/materials and avoid unnecessary unique draw calls.
4. Use instancing or batching for repeated objects where appropriate.
5. Prefer on-demand rendering when the scene can become idle; continuous frameloops require explicit justification.
6. Set conservative DPR bounds and scale quality for weaker devices.
7. Use progressive loading and meaningful fallback states for large assets.
8. Compress/optimize meshes and textures using the project-approved asset pipeline.
9. Limit post-processing, dynamic shadows, high-sample effects, and heavy transparent layers.
10. Avoid React state updates inside the render loop for rapidly changing scene values; use frame-local mutation patterns appropriate to R3F/Three.js.
11. Provide reduced-motion behavior for camera movement, parallax, auto-rotation, zoom, and large spatial transitions.
12. Test context loss/failure behavior and make sure the core page remains useful if the canvas cannot render.

## Anti-vibe-code requirements

- Do not add a floating sphere, globe, particle field, black hole, abstract blob, rotating device, or 3D object solely because it signals "premium" or "technology".
- Do not place important copy, navigation, forms, or required controls exclusively inside WebGL without an accessibility strategy.
- Do not add post-processing to compensate for weak art direction.
- Do not ship a desktop-quality scene unchanged to mobile.

## Output

- 3D admission decision
- Scene and DOM boundary
- Asset budget
- Rendering strategy
- Performance scaling plan
- Loading/fallback plan
- Reduced-motion behavior
- Accessibility/SEO notes
- Validation evidence and residual risk

## Trigger conditions

Use when introducing or materially changing Three.js, React Three Fiber, Drei, shaders, WebGL canvases, 3D scenes, 3D scroll sequences, model viewers, spatial product visualization, or persistent particle/scene effects.

## Dependencies

- `frontend-stack-selection`
- `interface-visual-direction`
- `motion-choreography`
- `web-performance-field-readiness`
- `accessibility-audit`

## Limitations

- Does not require 3D for premium design.
- Does not approve large assets or continuous rendering without measured justification.
- Does not replace specialist shader/graphics profiling where the project genuinely requires it.

## Validation

- Test representative low/mid/high device capability or an equivalent throttled profile.
- Measure loading impact and runtime frame stability.
- Verify idle scenes can stop rendering when architecture allows it.
- Verify DPR/quality degradation and fallback behavior.
- Verify canvas resize/orientation behavior and no layout breakage at supported viewports.
- Verify reduced-motion and non-WebGL experience remains coherent.
