# Interface Visual Direction — Asteria Residences

Capability: `interface-visual-direction`
Workflow: `site-from-brief-delivery` (step 2)

## Visual thesis

**The site is the drawing set, not the brochure.**

Asteria is twelve houses that do not exist yet. Everything a buyer can honestly be shown today is
what the architects have drawn: a survey of the ridge, twelve plots numbered 01–12, elevations,
sections, plans, orientation, and material samples. So the interface is built as a **working
architectural document** — measured, annotated, gridded, hairline-ruled, legible — that a serious
buyer reads the way they would read a drawing set, and not as a photographic mood board of a
building nobody has photographed.

This is the anti-generic move. Luxury property sites default to full-bleed dusk photography, a
centered serif headline, and a gradient scrim. Asteria has none of those, because it *cannot
truthfully have them*, and the constraint is turned into the brand.

Second thesis line, carried in the name: *Asteria* is the Titan of falling stars. The twelve plots
sit on the ridge in a fixed arrangement, and the site plan is drawn as a **constellation** — twelve
nodes, hairline connectors, numbered. That figure is the one signature graphic; it recurs at three
scales (page-level plan, section marker, favicon-scale glyph) and is never used as decoration
somewhere it means nothing.

## Hierarchy map

1. **Primary message** — where it is, what it is, how many, when it delivers. Stated in words and
   in the ridge datum figure, above the fold, at every viewport, no scroll required.
2. **Proof** — the twelve-plot index with real numbers. This is the second thing on the home page,
   before any lifestyle language, because the audience is comparing.
3. **Interaction focus** — one persistent, quiet call to action: *Request a visit*. One target, one
   verb, always the same words.
4. **Content rhythm** — dense fact blocks alternating with wide quiet bands. Never a uniform card
   wall.

## Grid and composition

- A **12-column grid** (twelve homes; the number is the grid) with a 1.5rem gutter, max content
  width 1360px, and a persistent left **margin rule** — a 1px hairline that runs down the page like
  a drawing sheet's trim line, carrying section numbers `01 / 02 / 03`.
- Deliberate asymmetry: primary content occupies columns 1–8 or 4–12; the residual column band
  carries annotations (coordinates, orientation, area) in small caps. Nothing is centered by
  default. The only centered element on the site is the residence index number in its plot marker.
- Section transitions are **ruled**, not faded: a hairline plus a section number plus a label. No
  gradient dividers, no blurred blobs.
- Density is intentionally *high* in fact regions (tabular, tight leading) and intentionally *low*
  in argument regions (short measure, generous leading). The contrast between the two is the rhythm.

## Typography

| Role | Family | Behaviour |
| --- | --- | --- |
| Display / statement | Fraunces (variable, optical size + soft axis) | Tight tracking, 100–140 optical size, weight 300–400. Never bold. Fluid clamp from 2.25rem to 5.5rem. |
| Body / editorial | Newsreader (variable) | 1.0625–1.1875rem, measure capped at 68ch, leading 1.65. |
| Annotation / data | IBM Plex Mono | 0.6875–0.8125rem, uppercase, letter-spacing 0.12em, tabular numerals. Carries every measurement, coordinate, index and label. |

The mono annotation layer is the tell that this is a drawing set. Numbers are always tabular so
columns of areas and prices align. All three families are self-hosted (`@fontsource-variable`),
subset to latin, `font-display: swap`, preloaded for the two above-the-fold faces.

## Colour, surface, material

Taken from the material palette of the actual project, not from a "luxury" swatch:

- `ink` `#14161a` — graphite, the drawing line and primary text
- `paper` `#f4f1ea` — warm drafting paper, the page
- `chalk` `#fbfaf7` — raised surfaces
- `limestone` `#c9bfae` — the cladding stone, used for rules and inactive states
- `oxide` `#8c4a2f` — the corten detail; the **only** accent, used for the active plot, focus rings,
  the CTA, and nothing else
- `slate` `#3d4550` — secondary text
- `moss` `#4a5b46` — the ridge planting; used only in the location surface's terrain figure

Surfaces are flat. Radii are 0 except a 2px softening on interactive controls. **No shadows**, no
glass, no glow, no gradient text. Depth is expressed by rule weight (0.5px / 1px / 2px) and by
paper vs chalk, exactly as a drawing expresses depth by line weight.

## Media direction

- **No photographs.** Media is a set of hand-authored SVG drawings generated as part of the build:
  ridge section, site plan, per-residence elevation, per-residence floor plan, orientation rose,
  material swatch tiles. Each is authored deterministically from the residence data, so the drawing
  and the numbers cannot disagree.
- Drawings are **structural**, not decorative: every one of them carries information stated nowhere
  else, and each has a real `<title>`/`<desc>` and a visible caption.
- Aspect ratios are fixed per drawing type (16:9 section, 4:3 plan, 3:2 elevation) so there is no
  layout shift and no art-direction crop problem.
- Raster imagery is absent by design, which is also why the mobile byte budget is small.

## Interaction and motion character

**Restrained and instrument-like.** The site should feel like a well-made measuring tool: things
respond immediately, land exactly, and never bounce.

- Hover/focus on a plot marker: 120ms colour and rule-weight change, plus the corresponding row in
  the index highlighting. Reciprocal, informational, no movement.
- The one narrative motion is the **ridge datum draw-on** in the hero: the section line strokes
  itself once, 900ms, on first paint. It is a drawing being drawn. It is not repeated on scroll and
  not applied to any other element.
- Section reveals: none. There is no fade-up-on-scroll anywhere on this site. That is a deliberate
  rejection of the default.
- `prefers-reduced-motion: reduce` → the datum line renders complete immediately, transitions
  collapse to 0ms, and no behaviour is lost.

## Signature moments

1. **The ridge datum** — a measured section of the ridge with the twelve plots pegged along it, drawn
   once on load, doubling as the hero image and as the site's primary orientation device.
2. **The plot index** — twelve numbered rows that are simultaneously a data table and a map legend,
   cross-highlighting with the constellation plan.
3. **The margin rule** — section numbering in the left margin, present on every page, that makes the
   whole site read as one continuous document.

## Anti-patterns explicitly rejected

- Centered hero + pill badge + gradient headline
- Equal-width card walls
- Bento grids
- Glassmorphism, glow, radial gradients, noise texture, star-field backgrounds
- Identical fade-up on every section
- Icon-in-circle feature lists
- Invented metrics, fake awards, fake testimonials, fake "3 units left" urgency
- Autoplay background video (also prohibited by the fixture)
- Stock photography standing in for a building that does not exist

## Implementation constraints (verifiable)

1. Accent `oxide` appears only on: focus ring, primary CTA, active plot, current nav item. Verified
   by grep over compiled CSS.
2. `border-radius` > 2px must not appear in any component style.
3. `box-shadow` must not appear in any component style.
4. Every drawing has `<title>` and either `role="img"` with a label or `aria-hidden` plus an adjacent
   text equivalent.
5. All motion sits behind a single `--motion-*` token set that the reduced-motion media query zeroes.
6. Body measure never exceeds 68ch; annotation type never below 0.6875rem.
7. Contrast: body/ink on paper ≥ 12:1, annotation slate on paper ≥ 7:1, oxide on paper ≥ 4.5:1 —
   verified numerically in the accessibility evidence.
