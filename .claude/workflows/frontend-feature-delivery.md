# Frontend Feature Delivery Workflow

## Trigger

A user-facing web surface is created, redesigned, materially restyled, or extended with meaningful visual, responsive, motion, media, or 3D behavior.

## Objective

Deliver a production-ready frontend that is technically correct, visually authored for the product, responsive across representative sizes, accessible, performant, and independently reviewed for craft quality.

## Inputs

- Task request, acceptance criteria, constraints, authority, and risk classification
- Product/brand intent and canonical project memory
- Current repository, framework, design system, dependencies, and existing visual language
- Relevant screenshots, references, content, media, analytics/device evidence, and integration constraints

## Sequence

1. **Inspect product and repository context**
   - Map the existing frontend architecture, dependencies, primitives, styles, media, routes, and visual patterns.
   - Preserve healthy existing behavior, integrations, and design-system contracts.

2. **Define visual direction**
   - Use `interface-visual-direction` for significant visual work.
   - Record hierarchy, composition, typography, media behavior, interaction character, signature moments, and anti-patterns to avoid.

3. **Select stack deliberately**
   - Use `frontend-stack-selection` before introducing or replacing frontend libraries.
   - Map CSS, Motion, GSAP, React Three Fiber/Three.js, primitives, and testing tools to concrete requirements.

4. **Plan component and design-system changes**
   - Reuse or extend existing components when appropriate.
   - Introduce tokens or primitives only when they represent stable semantic needs.

5. **Implement incrementally**
   - Build semantic, accessible, maintainable components.
   - Preserve integrations, loading/error states, keyboard behavior, and existing data contracts.

6. **Design motion where applicable**
   - Use `motion-choreography` for meaningful animation or scroll interaction.
   - CSS handles simple local transitions; Motion handles React-owned gestures/layout; GSAP handles complex timelines and ScrollTrigger narratives.
   - Reduced motion is part of implementation, not a post-release patch.

7. **Gate 3D where applicable**
   - Use `immersive-3d-experience` before introducing or materially expanding WebGL/R3F/Three.js.
   - Require narrative/interaction justification, adaptive quality, fallback, and mobile strategy.

8. **Audit responsive composition**
   - Use `responsive-layout-audit` across representative width and height classes.
   - Recompose layouts where necessary rather than mechanically stacking desktop UI.

9. **Produce visual evidence**
   - Use `visual-regression-review` or project-equivalent browser evidence.
   - Validate critical states, viewports, cropping, typography, spacing, fixed/sticky behavior, and overflow.

10. **Validate performance readiness**
   - Use `web-performance-field-readiness` when images, fonts, client JavaScript, third-party scripts, motion, video, or WebGL create material runtime cost.

11. **Independent frontend craft review**
   - A reviewer who did not solely own the implementation runs `frontend-craft-review` using `.claude/reviews/frontend-craft-review.md`.
   - Critical or High craft findings block approval.

12. **Deliver evidence and continuity**
   - Record changed assets, tests, browser evidence, review outcome, decisions, remaining risks, and durable memory updates when stable facts changed.

## Required lifecycle

1. **Understand** - Confirm outcome, scope, constraints, authority, audience, brand/product intent, and acceptance criteria.
2. **Inspect** - Read canonical memory, contracts, decisions, repository evidence, runtime declarations, and current frontend state.
3. **Plan** - Define ownership, dependencies, visual direction, stack choices, risks, validation, review gates, and rollback strategy.
4. **Execute** - Implement incrementally within scope while preserving existing behavior and source-of-truth boundaries.
5. **Validate** - Run code, browser, responsive, visual, accessibility, and performance checks proportionate to the change.
6. **Review** - Complete independent frontend craft and other applicable review gates.
7. **Document** - Record evidence, decisions, limitations, and stable memory changes.
8. **Deliver** - Report successful, conditional, blocked, or failed outcome based on actual gate results.

## Responsible agents

- `orchestrator`: route scope/risk and enforce independent gates.
- `frontend-engineer`: primary implementation owner.
- `ux-director`: visual/interaction hierarchy review and design direction where required.
- `design-system-engineer`: token/component-system ownership when shared primitives change.
- `performance-engineer`: performance review when runtime cost is material.
- `qa-engineer` or another independent reviewer: browser/visual validation and final craft evidence as assigned.

## Decision points

- Whether the change is small enough to skip explicit visual-direction work.
- Whether an existing dependency solves the problem before adding Motion, GSAP, R3F, or another library.
- Whether 3D passes the admission test.
- Whether desktop motion/visual behavior should be reduced, replaced, or removed on mobile.
- Whether visual differences are intentional and baseline-worthy or regressions.
- Whether the implementation feels authored for the product or remains generic/template-like.

## Mandatory gates for significant visual changes

- no unresolved critical responsive breakage
- no unexplained horizontal overflow or clipped primary action
- reduced-motion behavior validated when motion exists
- visual/browser evidence captured
- performance impact assessed when runtime-heavy features exist
- independent frontend craft review completed

## Failure handling

- Stop and report blocked when brand/product context, required assets, authority, or acceptance criteria are too incomplete to make a safe decision.
- Remove or simplify effects when they compromise readability, accessibility, responsiveness, or performance.
- Do not update screenshot baselines merely to suppress a regression failure.
- Do not self-approve unresolved Critical or High craft findings.
- Do not describe a frontend as premium, finished, or release-ready when required rendered evidence is missing.

## Completion criteria

- Functional acceptance criteria pass.
- Applicable frontend craft capabilities have either been completed or explicitly and defensibly marked not applicable.
- Browser/responsive evidence supports the result.
- Accessibility and reduced-motion requirements pass.
- Performance risk is within accepted budget or explicitly governed.
- Independent frontend craft review outcome is Approved or Approved with resolved/accepted conditions.
