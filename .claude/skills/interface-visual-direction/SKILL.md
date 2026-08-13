---
name: interface-visual-direction
description: "Define a distinctive visual direction before implementation when a user-facing surface needs premium hierarchy, composition, typography, rhythm, imagery, depth, and interaction intent."
---

# Interface Visual Direction Skill

## Purpose

Translate product, audience, brand, and content into an explicit visual thesis before implementation begins. The goal is to prevent technically correct interfaces from collapsing into generic AI-default composition.

## Inputs

- Product intent and audience
- Brand assets, tone, references, and constraints
- Existing interface and design system
- Content hierarchy and conversion priorities
- Required devices and accessibility expectations
- Existing screenshots, prototypes, or live implementation evidence

## Procedure

1. State the visual thesis in one or two sentences: what the interface should communicate before a user reads the copy.
2. Identify the dominant hierarchy: primary message, supporting proof, interaction focus, and content rhythm.
3. Define composition rules for grid, alignment, whitespace, density, section transitions, and intentional asymmetry where appropriate.
4. Define typography roles, scale relationships, line length, weight contrast, and responsive behavior.
5. Define image/media behavior: crop logic, aspect ratios, art direction, loading priority, and whether media is structural or decorative.
6. Define surface language: borders, radii, depth, shadows, materials, color relationships, and token usage.
7. Define interaction character: restrained, editorial, kinetic, tactile, cinematic, utilitarian, or another explicit direction.
8. Identify one or more signature moments that belong to the product or brand rather than to a generic frontend trend.
9. Identify patterns to avoid because they would make the result look templated, derivative, or disconnected from the product.
10. Produce implementation constraints that the frontend engineer can verify.

## Anti-default review

Do not allow the following to appear by default without a clear design rationale:

- Centered hero plus pill badge plus gradient headline as an automatic landing-page formula
- Repeated equal-width cards used to fill space
- Decorative bento grids without information-architecture value
- Glassmorphism, neon glow, radial gradients, star fields, or noise textures used as generic "premium" signals
- Random dashboard mockups or floating UI fragments without product meaning
- Identical fade-up animation on every section
- Excessive rounded containers that erase hierarchy
- Generic icon-in-circle feature lists
- Artificial social proof, invented metrics, or decorative data visualization
- Copy and layout borrowed from a reference instead of deriving a new system from the product

These patterns are not universally forbidden. They require a product, content, or brand justification and must survive independent craft review.

## Output

- Visual thesis
- Hierarchy map
- Grid and composition rules
- Typography direction
- Color/surface/media direction
- Interaction and motion character
- Signature moments
- Anti-patterns to avoid
- Responsive implications
- Implementation acceptance criteria

## Trigger conditions

Use before redesigning or significantly extending a marketing site, product shell, onboarding flow, portfolio, dashboard, or other user-facing surface where visual quality and differentiation matter.

## Dependencies

- `framework/frontend-craft-model.md`
- `content-quality-review`
- `design-token-architecture`
- `accessibility-audit`
- Current product and brand evidence

## Limitations

- Does not invent brand attributes, metrics, testimonials, or product claims.
- Does not require maximal visual complexity.
- Does not authorize copying a reference implementation.

## Validation

- The direction must be explainable without naming a trendy library or design gallery.
- Each major visual choice must support hierarchy, brand, content, interaction, or usability.
- Responsive behavior must preserve the visual thesis rather than simply stack desktop sections vertically.
- The final implementation must be reviewed against this direction by `frontend-craft-review`.
