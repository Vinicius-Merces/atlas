# Frontend Craft Review Gate

## Scope

Evaluate a significant user-facing frontend change for authored visual quality, responsive composition, purposeful motion/3D, performance-aware implementation, and resistance to generic template or AI-default patterns.

This gate is independent from functional correctness. A green build does not imply a green craft review.

## Required evidence

- Request and acceptance criteria
- Product/brand intent and current visual direction when applicable
- Implemented routes/states under review
- Representative rendered browser evidence
- Responsive audit evidence
- Visual-regression evidence where the repository supports it
- Motion/3D rationale and reduced-motion behavior when applicable
- Performance evidence for material runtime-heavy features
- Relevant implementation diff, tests, and contracts

Missing rendered evidence for a significant visual change prevents an Approved outcome.

## Review questions

### Visual authorship

- Can the interface's visual thesis be explained without naming a trend, library, or template?
- Does hierarchy read clearly before every line of copy is consumed?
- Does the interface feel specific to this product, audience, and brand?
- Are signature moments intentional and limited enough to remain meaningful?

### Composition

- Is spacing rhythm deliberate across sections and states?
- Do different content roles receive appropriately different compositions?
- Are empty space, asymmetry, alignment, and density intentional?
- Does the layout remain anchored and readable on large screens?

### Typography and media

- Are scale, weight, line length, wrapping, and contrast coherent?
- Do image/video crops preserve intended focal content at representative sizes?
- Are media and mockups real/authorized rather than invented visual filler?

### Components and design system

- Are library primitives meaningfully adapted to the product?
- Are radii, borders, surfaces, shadows, icons, and tokens coherent rather than copied defaults?
- Is component reuse appropriate without forcing unrelated content into identical cards?

### Motion

- Does each meaningful animation have a purpose?
- Are CSS, Motion, and GSAP responsibilities deliberate rather than overlapping?
- Are scroll pin/scrub effects usable and reversible on smaller screens?
- Is `prefers-reduced-motion` or project-equivalent behavior coherent?

### 3D/WebGL

- Does 3D communicate or enable something worth its cost?
- Are adaptive quality, mobile strategy, loading, fallback, and semantic DOM boundaries clear?
- Are decorative particles/globes/blobs/scenes being used as generic premium signals?

### Responsive quality

- Is mobile deliberately recomposed instead of merely stacked?
- Are intermediate widths free of accidental breakage?
- Are low-height laptops and very large desktops considered where relevant?
- Are primary actions, navigation, forms, and content usable by touch and keyboard?

### Anti-template / anti-AI-default

Flag unexplained or repetitive patterns such as:

- pill-badge centered hero formulas
- generic gradient-highlighted headline formulas
- unjustified bento grids
- glassmorphism/neon glow/radial gradients used as a universal premium shorthand
- icon-in-circle feature grids
- equal rounded cards for unrelated content
- floating dashboard/UI fragments without product meaning
- invented metrics or visualized data
- identical fade-up animation across every section
- excessive parallax/cursor/particle effects
- decorative 3D without narrative purpose
- visually untouched component-library defaults
- generic product copy that could belong to almost any SaaS/site

These patterns are findings when they lack defensible product, UX, content, or brand rationale, not merely because the pattern exists.

## Findings

Record each finding with:

- severity
- observed evidence
- affected viewport/state/path
- impact on trust, usability, differentiation, or polish
- recommended correction
- verification method

Also record strong authored patterns worth preserving so subsequent work does not erase successful design decisions.

## Severity

Use `.claude/contracts/review-contract.md`:

- Critical
- High
- Medium
- Low
- Note

Unresolved Critical or High findings block approval.

## Outcome

Record exactly one outcome:

- Approved
- Approved with conditions
- Changes required
- Blocked

The implementing agent may provide evidence and remediation, but must not be the sole approver of its own significant frontend craft work.
