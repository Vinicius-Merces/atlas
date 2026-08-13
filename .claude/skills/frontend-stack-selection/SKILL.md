---
name: frontend-stack-selection
description: "Select frontend libraries and rendering tools when a user-facing web change needs implementation or modernization, choosing CSS, Motion, GSAP, React Three Fiber, primitives, and supporting libraries by evidence rather than trend."
---

# Frontend Stack Selection Skill

## Purpose

Choose the smallest, strongest frontend stack that matches the product intent, existing repository, interaction model, performance budget, accessibility requirements, and maintenance constraints.

The objective is not to maximize dependencies. The objective is to make deliberate technical choices that support a distinctive, production-ready interface without creating a trend-driven or template-driven result.

## Inputs

- Product and brand intent
- Existing framework, dependencies, design system, and component primitives
- Interaction and motion requirements
- Browser/device support expectations
- Performance and accessibility constraints
- Existing implementation patterns and project memory

## Decision hierarchy

1. Preserve a healthy existing stack before proposing replacement.
2. Use platform CSS for simple, local, self-contained transitions and effects.
3. Prefer Motion for React-owned gestures, layout transitions, shared layout, enter/exit states, and component-level animation.
4. Prefer GSAP for coordinated timelines, complex sequencing, ScrollTrigger-driven narratives, pinning, scrubbing, or animation that spans multiple components and DOM regions.
5. Use Three.js or React Three Fiber only when real spatial rendering, 3D interaction, or narrative depth is part of the experience rather than decorative novelty.
6. Use Drei or other helpers only when they reduce implementation risk or repeated boilerplate without hiding critical performance behavior.
7. Reuse existing accessible primitives such as Base UI, Radix, React Aria, or the project-native equivalent before inventing controls from scratch.
8. Do not install a library for a behavior that the current stack or browser platform already solves cleanly.

## Procedure

1. Inspect package manifests, framework version, styling architecture, component library, animation libraries, 3D/WebGL dependencies, testing stack, and build constraints.
2. Identify the actual interface problem before naming a library.
3. Separate requirements into static layout, stateful interaction, layout transition, timeline animation, scroll choreography, 3D rendering, and browser validation.
4. Map each requirement to the least complex suitable tool.
5. Check bundle cost, runtime cost, SSR/hydration implications, cleanup requirements, reduced-motion behavior, and mobile fallback.
6. Reject duplicate libraries that solve the same problem unless migration or interoperability is explicitly justified.
7. Record the selected tool, rejected alternatives, and the reason for each decision.
8. Escalate to architecture or performance review when the choice introduces WebGL, substantial client JavaScript, persistent animation loops, or a new cross-project dependency.

## Anti-vibe-code requirements

- Never choose a library because it is fashionable, visually impressive in isolation, or common in AI-generated examples.
- Never add GSAP, Motion, or React Three Fiber merely to make a page feel "premium".
- Do not default to shadcn-style composition, bento grids, glass cards, gradients, glow, or animated hero effects without a product or brand reason.
- Prefer one coherent motion/rendering strategy over overlapping animation systems with unclear ownership.
- Preserve a strong existing visual language instead of replacing it with a generic starter-kit aesthetic.

## Output

- Existing stack assessment
- Requirements-to-tool matrix
- Selected libraries and platform capabilities
- Rejected alternatives with reasons
- Bundle/runtime/accessibility implications
- Migration or interoperability notes
- Validation plan

## Trigger conditions

Use when implementing or modernizing a significant frontend surface, selecting animation/rendering libraries, introducing a component primitive system, or deciding whether GSAP, Motion, Three.js/R3F, or related dependencies are justified.

## Dependencies

- `framework/frontend-craft-model.md`
- `component-reuse-assessment`
- `dependency-impact-analysis`
- `performance-budget-analysis`
- Current repository evidence and project memory

## Limitations

- Does not authorize dependency installation without task scope and repository evidence.
- Does not treat any named library as mandatory.
- Does not replace independent accessibility, performance, QA, or frontend craft review.

## Validation

- Every new dependency must map to a concrete requirement that existing capabilities do not solve adequately.
- Confirm cleanup/lifecycle behavior for imperative animation systems.
- Confirm reduced-motion strategy for non-essential movement.
- Confirm fallback or quality-scaling strategy for WebGL/3D.
- Record the final decision and residual risks.
