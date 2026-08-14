# Frontend Craft Model

## Purpose

The ATLAS Frontend Craft Model defines the quality bar for user-facing web work that must feel intentionally designed, engineered, and authored for its product rather than assembled from popular UI defaults.

Functional correctness is necessary but not sufficient. A frontend can pass build, type checking, accessibility automation, and performance checks while still presenting weak hierarchy, generic composition, trend-driven decoration, or visually inconsistent responsive states.

This model makes frontend craft an explicit system concern.

## Core principle

**Design intent before implementation, tool choice after intent, evidence before approval.**

ATLAS must not equate premium quality with more animation, more dependencies, more WebGL, darker backgrounds, larger gradients, or a particular component library. Premium frontend quality comes from coherent hierarchy, distinctive authorship, appropriate interaction, strong responsive composition, and disciplined execution.

## Premium delivery contract

When the brief uses language such as premium, bespoke, high-end, studio-grade, memorable, cinematic, or "must not look vibe-coded", the frontend owner must create a compact direction record before implementation. It must define:

1. a product-specific visual thesis derived from the subject's real vocabulary, tools, materials, data, or workflow;
2. one justified aesthetic risk and one signature moment that could not be relabeled for an unrelated product;
3. hierarchy, density, grid, typography, surface, color, iconography, and responsive composition rules;
4. a motion inventory covering state feedback, spatial continuity, and emphasis, or an explicit rationale for a deliberately static interface;
5. loading, empty, error, success, focus, disabled, destructive, and long-content states applicable to the surface;
6. rendered acceptance evidence at the declared viewport matrix.

The direction record can live in a design-system document, implementation plan, evidence packet, or project memory. It must be inspectable; adjectives in a prompt do not satisfy it.

An interactive product surface should not ship with zero interaction feedback. At minimum, navigation, mutation feedback, focus, loading, and state change need coherent visual behavior. Motion must remain purposeful and reduced-motion safe; this rule does not require decorative animation.

## Capability sequence

For significant user-facing work, ATLAS should use the following sequence proportionate to scope:

1. `interface-visual-direction`
2. `frontend-stack-selection`
3. existing design-system and component-reuse capabilities
4. implementation by `frontend-engineer`
5. `motion-choreography` when meaningful motion exists
6. `immersive-3d-experience` when WebGL/3D is justified
7. `responsive-layout-audit`
8. `visual-regression-review`
9. `web-performance-field-readiness`
10. independent `frontend-craft-review`

Not every task needs every capability. The orchestrator and frontend owner must record why a capability is applicable or intentionally skipped.

## Frontend stack policy

### CSS and browser platform

Use CSS and native platform features first when the behavior is local, simple, maintainable, and does not require a richer state or sequencing model.

### Motion

Prefer Motion for React-centric interaction where animation belongs to component state or layout semantics, including:

- enter/exit states
- gestures such as hover, tap, focus, and drag
- layout and shared-layout transitions
- component-scoped scroll or in-view behavior
- springs and interruptible interaction feedback

### GSAP

Prefer GSAP when temporal orchestration is the problem, including:

- coordinated timelines
- complex multi-element sequencing
- ScrollTrigger narratives
- pinning, scrubbing, snapping, and long-form scroll choreography
- imperative animation spanning multiple DOM regions

GSAP usage in React must be scoped and lifecycle-safe. Global unmanaged selectors, stale timelines, and listeners that survive unmount are not acceptable.

### Three.js / React Three Fiber

Use Three.js or React Three Fiber only when real spatial rendering materially contributes to product understanding, interaction, storytelling, or brand expression.

3D must have:

- an explicit admission rationale
- DOM/Canvas boundary
- asset and draw-call budget
- DPR/quality strategy
- loading and fallback behavior
- reduced-motion behavior
- weak-device/mobile strategy
- a coherent non-WebGL experience when core content must remain available

R3F does not make an interface premium by itself.

## Anti-vibe-code standard

ATLAS must challenge visual patterns that appear because they are common in templates, component galleries, AI generations, or recent trends rather than because the product needs them.

The following patterns require explicit justification when used prominently or repeatedly:

- centered hero with pill badge and generic gradient-highlighted headline
- bento grid without information-architecture value
- repeated equal-weight rounded cards for unrelated content
- glassmorphism, neon glow, radial gradients, particle fields, or noise used as generic premium signals
- icon-in-circle feature grids
- floating dashboard fragments with no product meaning
- arbitrary device mockups or fake UI screenshots
- identical `fade-up`/stagger behavior across every section
- parallax on content that has no spatial relationship
- custom cursor effects that interfere with normal pointer feedback
- decorative 3D objects, globes, blobs, spheres, portals, black holes, or particle scenes without narrative purpose
- invented metrics, testimonials, dashboards, charts, or product states used to fill visual space
- visually untouched library defaults presented as bespoke design

These are not categorical bans. The review question is whether the pattern has a defensible product, brand, UX, or content reason and whether it is executed coherently.

## Authorship requirements

A significant frontend should be able to answer:

- What is the visual thesis?
- What is the hierarchy before copy is read?
- What makes this interface belong to this product?
- What is deliberately repeated, and what is deliberately varied?
- What are the signature moments?
- Why does each animation exist?
- Why is each major dependency needed?
- How does the composition change on mobile and large screens?
- What happens with reduced motion, weak devices, slow networks, or failed WebGL?

If those answers are missing, implementation should not be described as premium or finished.

### Operational SaaS authorship

For dashboards and business systems, authorship must come from the product's operating model rather than marketing-page spectacle. Prefer a product-specific command surface, meaningful density, exception-first status color, tabular changing numbers, strong table/form/detail composition, and transitions that clarify state. A generic sidebar plus KPI cards plus a table is a shell, not a finished direction.

Use a restrained token grammar by default:

- one dominant accent plus semantic status colors;
- an explicit spatial rhythm, commonly an 8 px-derived scale;
- layered low-opacity shadows from one light direction;
- related nested radii rather than arbitrary rounded containers;
- iconography from one visual family, without emoji or repeated icon-in-chip decoration;
- color to signal priority or exception, not to rainbow-code ordinary rows.

## Responsive craft

Responsive behavior must preserve intent, not only fit.

ATLAS should validate representative small phone, common phone, tablet, laptop, desktop, and large-desktop states, including height-constrained laptops where heroes, sticky content, modals, and pinned sequences often fail.

Mobile composition may change ordering, density, media crop, motion strategy, navigation model, and interaction affordances. Mechanical stacking is not automatically acceptable.

Large screens must also be reviewed for excessive line length, weak anchoring, empty dead zones, oversized components, and loss of visual hierarchy.

## Motion accessibility

Non-essential motion must honor `prefers-reduced-motion` or the project-equivalent accessibility mechanism.

Reduced motion should preserve information and interaction while removing or substantially toning down large translation, scale, rotation, camera movement, parallax, and continuous animation that can create discomfort.

Reduced motion is not a late CSS patch. It is part of the motion design.

## Performance as design

Visual ambition must operate inside an explicit performance budget.

Particular scrutiny is required for:

- large hero images/video
- custom fonts and many font weights
- GSAP/scroll observers and persistent timelines
- Motion-heavy component trees
- WebGL/R3F scenes and continuous frameloops
- high DPR rendering
- large models/textures/HDRI
- post-processing
- third-party scripts
- duplicated animation or component libraries

Where a rich experience cannot fit all devices equally, use progressive enhancement and adaptive quality rather than shipping the same cost everywhere.

## Browser evidence

Meaningful visual changes require rendered evidence. Depending on project tooling, this may include:

- browser inspection
- deterministic screenshots
- Playwright `toHaveScreenshot` or equivalent visual regression tests
- viewport matrices
- interaction recordings
- performance traces

A successful build is not visual evidence.

## Independent craft gate

The implementing agent must not be the sole authority for frontend craft approval.

For significant frontend changes, an independent review should use `.claude/reviews/frontend-craft-review.md` and the `frontend-craft-review` skill. Critical or High craft findings block an Approved outcome until resolved or explicitly waived by authorized project governance.

## Source and runtime model

Claude Code remains the canonical skill source under `.claude/skills/`. Codex-native skill wrappers under `.agents/skills/` must point back to canonical instructions so stack guidance, visual standards, and review criteria do not drift across runtimes.

Obsidian/navigation artifacts may expose this model, but they do not become a second source of truth.
