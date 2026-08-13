---
name: frontend-craft-review
description: "Independently review a frontend for visual craft and anti-template quality when implementation is functionally complete but must not look generic, derivative, or AI-default."
---

# Frontend Craft Review Skill

## Purpose

Judge whether a frontend looks intentionally designed and engineered for its product, not merely assembled from popular components, default patterns, and fashionable effects.

This is an independent quality gate. Passing build, lint, tests, accessibility checks, or Lighthouse does not automatically satisfy frontend craft.

## Inputs

- Product and brand intent
- `interface-visual-direction` output when available
- Implemented routes and interaction states
- Responsive and visual-regression evidence
- Motion/3D rationale where present
- Existing design system and repository history

## Review dimensions

### 1. Visual thesis
- Is there a clear visual idea that can be described without naming a library, template, or trend?
- Does the page communicate hierarchy before the user reads every sentence?
- Is the composition appropriate to the audience and product?

### 2. Composition and rhythm
- Do section shapes, whitespace, alignment, and density create deliberate pacing?
- Are sections meaningfully different when their content roles differ?
- Are large empty areas intentional rather than artifacts of weak composition?
- Does the layout remain anchored on very large screens?

### 3. Typography and content hierarchy
- Are type scale, line length, weight, contrast, and spacing purposeful?
- Does copy fit the visual hierarchy instead of being poured into components?
- Are headings and supporting text sized for the actual viewport, not only a design screenshot?

### 4. Component authorship
- Do components feel adapted to the product rather than unchanged library defaults?
- Are tokens, radii, borders, shadows, controls, and iconography coherent?
- Is reuse balanced with the need for distinctive signature moments?

### 5. Motion authorship
- Does motion explain state, continuity, emphasis, or narrative?
- Are timing and easing varied by semantic role rather than copied across the page?
- Are GSAP/Motion choices justified and lifecycle-safe?
- Is reduced motion coherent rather than a broken version of the full experience?

### 6. 3D and visual effects
- Does WebGL/3D add meaning or merely signal "premium"?
- Are effects restrained enough that content remains primary?
- Is quality scaled for weaker devices and mobile?

### 7. Responsive authorship
- Is mobile a recomposed design rather than desktop stacked vertically?
- Do image crops, typography, navigation, motion, and spacing remain intentional across widths/heights?

### 8. Anti-template / anti-AI-default audit
Flag repeated or unexplained use of:

- centered pill-badge hero formulas
- gradient-highlighted generic headlines
- bento grids without information value
- glass cards and neon glow without brand logic
- icon-in-circle feature grids
- identical rounded cards for unrelated content
- random floating dashboard fragments
- fake product screenshots or invented metrics
- repeated fade-up/stagger on every section
- excessive parallax, cursor effects, particles, or 3D decoration
- stock copy such as generic transformation/innovation promises with no product specificity
- obvious library defaults left visually untouched

These are not banned categorically. A finding exists when the pattern lacks product, UX, content, or brand justification.

## Procedure

1. Review the live/rendered interface before reading implementation details when possible.
2. Compare implementation against product intent and visual direction.
3. Review representative mobile, laptop, desktop, and large-screen states.
4. Inspect motion and 3D in context, not from code alone.
5. Identify generic patterns, compositional repetition, weak hierarchy, and unearned effects.
6. Distinguish subjective preference from evidence-backed craft issues.
7. Rank findings by impact on trust, usability, differentiation, and polish.
8. Require remediation for Critical/High craft failures before approval.

## Output

- Craft review outcome
- Findings with severity and evidence
- Generic/derivative pattern findings
- Strong authored patterns worth preserving
- Responsive/motion/3D findings
- Required changes
- Residual risks

## Trigger conditions

Use as an independent gate for significant marketing sites, portfolios, public product surfaces, premium landing pages, redesigns, visually differentiated SaaS shells, and any task whose acceptance criteria include polished, premium, branded, bespoke, or agency-level frontend quality.

## Dependencies

- `framework/frontend-craft-model.md`
- `interface-visual-direction`
- `responsive-layout-audit`
- `visual-regression-review`
- `motion-choreography` when motion exists
- `immersive-3d-experience` when 3D exists

## Limitations

- Does not require visual complexity or animation.
- Does not substitute personal taste for evidence.
- Does not authorize copying a reference site.
- Does not self-approve implementation owned by the same agent/workstream.

## Validation

Approval requires enough rendered evidence to assess the relevant viewport and interaction states. Missing browser evidence for a meaningful visual change produces a conditional or blocked outcome rather than assumed success.
