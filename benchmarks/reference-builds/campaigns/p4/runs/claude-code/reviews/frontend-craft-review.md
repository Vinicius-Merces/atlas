# Frontend Craft Review — Asteria Residences (P4 reference build)

- **Reviewer:** Independent Frontend Craft reviewer (claude-code subagent, did not implement)
- **Date:** 2026-08-13
- **Run:** `benchmarks/reference-builds/campaigns/p4/runs/claude-code`
- **Branch:** `bench/p4-asteria-claude-code`
- **Commit:** `bff3259` (base `3ccdf6e`)
- **Fixture:** `benchmarks/reference-builds/specs/premium-marketing-site.yaml`
- **Axis:** `frontend_craft` — checks `marketing-visual-thesis`, `marketing-responsive` (blocking),
  `marketing-accessibility` (blocking), `marketing-motion-purpose`, `marketing-visual-regression`
- **Gate:** `.claude/reviews/frontend-craft-review.md`
- **Skills applied:** `frontend-craft-review`, `interface-visual-direction` (anti-default list),
  `responsive-layout-audit`, `accessibility-audit`, `visual-regression-review`, `motion-choreography`

## Method

Screenshots were opened and inspected as images (including native-resolution crops of the phone and
tablet captures, since the committed PNGs are 2–3× DPR and 12k–28k px tall). Implementation claims in
`planning/02-visual-direction.md` were treated as claims and re-verified by grep over
`site/app/tokens.css`, `site/app/globals.css` and `site/components/**`. Contrast ratios quoted below
were recomputed independently from the token values, not copied from the run's evidence.

Images inspected: `evidence/visual-regression/home--{phone-360,tablet-768,laptop-1280,wide-1920}.png`,
`residences--tablet-768.png`, `residence-detail--laptop-1280.png`, `enquire--{phone-360,laptop-1280}.png`,
`journal-entry--laptop-1280.png`, `location--tablet-768.png`, and
`evidence/browser/{05-enquire-success,06-validation-empty,09-store-failure,16-empty-state}.png`.

## Per-check verdicts

### 1. `marketing-visual-thesis` — **pass**

The thesis ("the site is the drawing set, not the brochure") is real in the render, not only in the
planning document. `home--wide-1920.png` opens with a left-anchored Fraunces statement, a mono
annotation datum line (`01 ALTO DA PEDRA … 148–178 M`), a tabular fact block, and a measured ridge
section with twelve pegged plots — no centered pill badge, no gradient scrim, no stock dusk
photography. `residence-detail--laptop-1280.png` carries schematic elevation, two floor plans, a
schedule of areas that foots to a total, a construction/systems list and four named material swatches;
`journal-entry--laptop-1280.png` is a genuinely editorial two-density layout with a two-column
density comparison table and a pull quote. Copy is product-specific and honest ("Nothing here is
photographed, because nothing is finished"), sold and reserved units stay in the index, and no
invented awards, testimonials or scarcity counters appear.

Anti-default audit against the `interface-visual-direction` list: `grep -rn "box-shadow" app components`
returns nothing; the only `border-radius` in the codebase is `var(--radius-control)` = `2px`
(`app/tokens.css:82`, 3 call sites); there is no glass, glow, radial gradient, noise, bento grid,
icon-in-circle grid, floating UI fragment or gradient headline. The one accented word ("drawn") is
flat `#8c4a2f`, not a gradient. This is the strongest dimension of the build.

Weaknesses, none disqualifying: `/residences` (`residences--tablet-768.png`) is a uniform twelve-item
bordered card grid — the weakest composition on the site and in tension with the direction's own
"never a uniform card wall"; the same data is better authored as the ruled table on the home page.
The index section at 1920 (`home--wide-1920.png`) leaves roughly 900 px of empty column beside a
twelve-row table because the site-plan figure is short and top-aligned, and the filtered-empty state
(`16-empty-state.png`) leaves a comparable void to the right of a 135 px filter column. Both read as
unresolved rather than as the intentional asymmetry the direction describes.

### 2. `marketing-responsive` (BLOCKING) — **partial**

Verified from all 40 `evidence/responsive/measure--*.json` files: `horizontalOverflow` is 0 and
`overflowingSelectors` and `smallTapTargets` are empty on every one of the 8 routes × 5 viewports.
Mobile is genuinely recomposed rather than stacked — `home--phone-360.png` converts the ruled index
table into stacked annotated rows and moves the site plan below the table; `enquire--phone-360.png`
keeps 48 px minimum control height, per-field hints and a real fieldset rhythm.

Deductions:

- The SVG drawings do not art-direct. Text inside them is fixed at 10–12 user units in a 1200-wide
  viewBox (`components/drawings/drawings.module.css:16,53,74,81,142`), so at 360 CSS px the ridge
  section's tick labels render at ≈2.9–3.2 px and at 768 px at ≈6 px. Confirmed by native-resolution
  crops of `home--phone-360.png` (fig. 01) and `home--tablet-768.png` (fig. 02). This also breaks the
  direction's constraint 6 ("annotation type never below 0.6875rem").
- Interactive plot links in the site plan are `display: none` below 48rem
  (`drawings.module.css:149-156`) while `app/location/page.tsx:101` still tells every user "Select any
  plot to open its residence". Function is hidden on mobile rather than recomposed.
- Measured line length reaches 80ch on 7 route/viewport combinations (`measure--location--laptop-1280.json`,
  `measure--privacy--wide-1920.json`, `measure--journal-entry--tablet-768.json`,
  `measure--home--tablet-768.json`), against a stated cap of 68ch.
- Coverage gaps versus `responsive-layout-audit`: no ~320 px small phone, no height-constrained case,
  no 1024/1440 intermediate widths.

### 3. `marketing-accessibility` (BLOCKING) — **partial**

Strong automated and semi-manual base: `evidence/accessibility/axe--*.json` shows zero violations on
all 14 routes plus `axe--enquire-validation-state.json` and `axe--enquire-success-state.json` (48
passes each) under `wcag2a/2aa/21a/21aa/22aa/best-practice`. `structure.json` confirms `lang=en-GB`,
one `h1`, `main` landmark and no skipped heading levels on six routes. `focus-indicators.json` records
a 2 px `rgb(140,74,47)` outline on all 40 sampled controls. `reduced-motion.json` shows the draw
animation resolving to `none` / `0px` dash-offset and every motion token at `0s`.
`drawing-alternatives.json` shows `role="img"`/`role="group"` with `aria-labelledby`, real `<title>`
and 201–917-character `<desc>` on the meaningful drawings and `aria-hidden` on the wordmark glyph.
`keyboard-order.json` shows "Skip to content" as the first stop with a sensible sequence.
`06-validation-empty.png` shows a linked error summary, per-field errors with a `▲` glyph plus text
(not colour alone), and `09-store-failure.png` preserves user input on server failure.

What the automation did **not** catch, and why this is not a pass:

- **SC 1.4.11 non-text contrast fails on the primary conversion flow.** `--rule-color` resolves to
  `#a19a8d` (`color-mix(limestone 78%, ink 22%)`, `tokens.css:34`) = **2.47:1 on paper, 2.67:1 on
  chalk**. It is the sole visual boundary of every form field (`enquire-form.module.css:63`, input fill
  `--chalk` is 1.08:1 against the `--paper` page) and of the secondary/ghost button
  (`globals.css:246-250`, e.g. "REQUEST A VISIT" in the hero). axe does not test 1.4.11, and
  `contrast.json` measures only nine text/background token pairs — no UI-boundary pair at all.
- axe reported `color-contrast` **incomplete** on 47 nodes (home), 71 and 72 nodes (residence detail /
  sold), 15 (location, residences) and 6 (filtered). These are the in-drawing labels; they were never
  triaged manually, so contrast inside the drawings is unverified rather than verified.
- The ~3 px drawing labels at 360 px (see check 2) are a legibility barrier even though the same
  figures are duplicated as text in the index table and `<desc>`.
- `#main` (the skip-link target) has no `scroll-margin-top` while the header is `position: sticky`
  (`site-chrome.module.css:4`); only `location.module.css:73` sets an offset. Risk against WCAG 2.2
  SC 2.4.11 (focus not obscured) for skip-link and anchor jumps.

### 4. `marketing-motion-purpose` — **pass**

Motion is unusually disciplined and matches the stated "instrument-like" character. The entire site
contains exactly one `@keyframes` (`drawings.module.css:35`, the ridge stroke draw-on) and eight short
`transition` declarations, all `120ms` on colour/fill/border only — no transform or layout animation,
no scroll reveals, no parallax, no cursor effects, no 3D. `app/page.tsx:106` passes `animate` only on
the home hero; `app/residences/[slug]/page.tsx:278` renders the same component without it, so the
signature moment is not diluted. All durations resolve through the single `--motion-*` token set,
zeroed by `prefers-reduced-motion` (`tokens.css:88-95`), with a belt-and-braces global override
(`globals.css:16-27`) and `scroll-behavior` falling back to `auto` — evidenced numerically in
`reduced-motion.json`. Only residual note: the plot-marker hover cross-highlight (`drawings.module.css:92`)
has a keyboard equivalent via `:focus-visible` only where the hit areas exist, i.e. not below 768 px
(see finding B3).

### 5. `marketing-visual-regression` — **partial**

`tests/responsive.spec.ts` produces the 40 PNGs deterministically enough for review: fixed viewport and
`deviceScaleFactor` per class, `networkidle`, an injected
`*{animation:none!important;transition:none!important}` style tag, `animations: "disabled"` on capture,
`fullPage: true`, self-hosted fonts, and content authored from static data files. The five-viewport ×
eight-route matrix is honest, and the accompanying JSON turns each capture into assertions rather than
vibes.

But this is capture, not regression: there is no `toHaveScreenshot`, no committed baseline and no
diffing anywhere in the suite, so a future layout regression would not be detected — only re-reviewed
by a human. The matrix also omits states the `visual-regression-review` skill lists as required:
form error, form success, filtered-empty, 404 and a reduced-motion capture are absent from the
viewport matrix and exist only as single-viewport `evidence/browser/*.png`. Those browser PNGs are
weaker composition evidence because they were taken mid-journey with sticky chrome: in
`06-validation-empty.png` the site header renders across the middle of the page (y ≈ 1128) and the
sticky FAQ aside floats ~750 px below its real position — the same artefact appears in
`05-enquire-success.png` and `09-store-failure.png`.

## Findings

### Blocking

**B1 — High — Non-text contrast of every form field and secondary button is 2.47:1 (WCAG 2.2 AA
SC 1.4.11).**
Evidence: `site/app/tokens.css:34` (`--rule-color` → `#a19a8d`), `site/components/enquire-form.module.css:63`,
`site/app/globals.css:246-250`; recomputed ratios 2.47:1 on `--paper`, 2.67:1 on `--chalk`; input fill vs
page 1.08:1. Affects `/enquire` at all viewports (`enquire--laptop-1280.png`, `enquire--phone-360.png`)
and the hero ghost CTA on every page. Impact: low-vision users cannot reliably locate field boundaries
in the site's only conversion path; the failure is invisible to axe and to the run's own
`contrast.json`.
Fix: introduce a dedicated interactive boundary token at ≥3:1 (e.g. `color-mix(in srgb, var(--limestone) 55%, var(--ink) 45%)`
≈ `#6f6a61`, 3.4:1 on paper) for `.input`, `.button--ghost`, checkbox and select borders, keeping the
hairline `--rule-color` for purely decorative sheet rules.
Verification: extend `tests/accessibility.spec.ts` with a computed non-text-contrast assertion over
input/button border colours vs their adjacent background, and re-capture `enquire--*`.

### Non-blocking

**N1 — Medium — Drawing labels are ~3 px at 360 px and ~6 px at 768 px.**
Evidence: `components/drawings/drawings.module.css:16,53,74,81,142` (fixed 10–12 unit text in a
1200-wide viewBox); native crops of `home--phone-360.png` and `home--tablet-768.png`. Also contradicts
direction constraint 6. Impact: the site's signature media is decorative rather than readable on the
majority viewport class; mitigated only because the same numbers appear in the index table and `<desc>`.
Fix: ship a mobile variant of `RidgeSection`/`SitePlan` with a reduced label set and label sizes scaled
by the inverse of the render scale (or `vector-effect`-style non-scaling text), or drop labels below
768 px and state the caption as the alternative.
Verification: re-capture phone/tablet and assert rendered label height ≥ 11 px via `getBoundingClientRect`.

**N2 — Medium — Site-plan interaction removed below 768 px while the copy still instructs it.**
Evidence: `drawings.module.css:149-156` (`.planHits { display: none }` until 48rem) versus
`app/location/page.tsx:101` ("Select any plot to open its residence"); `location--tablet-768.png`
shows the affordance present at 768 only. Impact: hidden functionality on mobile plus a false
instruction; keyboard users at narrow widths lose the plot links entirely.
Fix: render the hit areas at all widths with ≥24 px touch targets, or make the sentence conditional and
point to the index list.
Verification: keyboard-order capture at 360 px showing the twelve plot links, or updated copy.

**N3 — Medium — Measure exceeds the stated 68ch cap; the test threshold was set to 80.**
Evidence: `measure--location--laptop-1280.json`, `measure--privacy--wide-1920.json`,
`measure--journal-entry--tablet-768.json`, `measure--home--tablet-768.json` all report
`longestLineChars: 80`; `tests/responsive.spec.ts` asserts `toBeLessThanOrEqual(80)` while
`planning/02-visual-direction.md` constraint 6 claims ≤68ch. The overruns are list items and definition
descriptions, which never receive `var(--measure)` (only 5 call sites).
Fix: apply the measure cap to prose `li`/`dd` containers and tighten the assertion to 68 (or amend the
stated constraint honestly).

**N4 — Medium — Direction constraint 1 (accent allowlist) is not true as written.**
Evidence: 30+ `var(--accent)` declarations across `app/**` and `components/**`, including the required
asterisk (`enquire-form.module.css:53`), margin section numbers (`globals.css:201`), the hero word
"drawn" (`page.module.css:48`), pull-quote and error left rules
(`blocks.module.css:48`, `enquire-form.module.css:197,213`), journal counts and plan-family counts.
Pixel-sampled `enquire--phone-360.png` confirms `#8c4a2f` on the required asterisk. Impact: the usage is
still restrained and semantic, so this is not a craft failure — but the constraint is stated as
"verified by grep" and would not survive that grep, which weakens every other claim in the document.
Fix: rewrite the constraint to the real allowlist and back it with an actual CSS-token test, or reduce
accent usage to the four declared roles.

**N5 — Medium — Visual-regression suite has no baselines and omits required states.**
Evidence: `tests/responsive.spec.ts` uses `page.screenshot` only, no `toHaveScreenshot`/baseline/diff;
error, success, filtered-empty, 404 and reduced-motion states are absent from the viewport matrix.
Sticky-chrome artefacts in `06-validation-empty.png` (header rendered mid-page at y≈1128) make the
substitute browser evidence unreliable for composition judgement.
Fix: add `toHaveScreenshot` with committed baselines for a core subset, add the missing states to the
matrix, and scroll to top / neutralise `position: sticky` before full-page capture.

**N6 — Low — Responsive matrix omits ~320 px, height-constrained, and 1024/1440 intermediate cases.**
Evidence: `VIEWPORTS` in `tests/responsive.spec.ts` (360/414/768/1280/1920, all default heights) versus
the `responsive-layout-audit` required coverage.
Fix: add 320×568 and 1440×720; assert no sticky-header/aside collision at low height.

**N7 — Low — axe `color-contrast` incomplete results were never triaged.**
Evidence: `axe--home.json` (47 nodes), `axe--residence-detail.json` (71), `axe--residence-sold.json` (72),
`axe--location.json` / `axe--residences.json` (15), `axe--residences-filtered.json` (6).
Fix: sample the computed fill of in-drawing text against its actual backdrop and record the ratios in
`contrast.json`, or document why each incomplete node is out of scope.

**N8 — Low — Sticky header can obscure skip-link and anchor targets (WCAG 2.2 SC 2.4.11).**
Evidence: `components/site-chrome.module.css:4` sticky header, `app/layout.tsx:40` skip link to `#main`,
`scroll-margin-top` present only at `app/location/location.module.css:73`.
Fix: set `scroll-margin-top` on `#main` and all anchor targets from a shared header-height token.

**N9 — Note — Submitting/disabled button label is 2.6:1.**
Evidence: `globals.css:239-244` (`--limestone-deep` `#a89c88` with `#fdfaf7` text). Disabled controls are
exempt from AA, but this is the in-flight submit state users actually read.
Fix: keep the accent background and dim only the label, or add a mono "SENDING…" state at ≥4.5:1.

**N10 — Note — Placeholder clipped on phone.** "e.g. weekday mornings, or the 14th–16th" is cut mid-word in
`enquire--phone-360.png`; shorten the placeholder (the hint below already carries the detail).

**N11 — Note — `/residences` card wall.** `residences--tablet-768.png` renders twelve visually identical
bordered blocks, which the direction explicitly rejects; consider reusing the home page's ruled table
composition with the drawing thumbnails as the differentiator.

## Strong authored patterns worth preserving

- The drawing-set thesis and its honesty constraint (no photography because nothing is built) — the
  single strongest anti-default decision in the build.
- The mono annotation layer with tabular numerals and the left margin rule with section numbering;
  ruled (not faded) section transitions.
- One narrative animation, zero scroll reveals, all timing through one token set — this is the correct
  reading of `motion-choreography` and should not be "improved" with fade-ups later.
- Density contrast between fact regions (index, schedule of areas, journey table) and argument regions
  (short-measure editorial), rather than uniform section rhythm.
- Sold/reserved units left visible; no invented metrics, awards or urgency; failure state that says
  plainly "Your request was NOT recorded" and preserves input.
- The evidence discipline itself: 40 measured captures with assertions, 16 axe states, structure,
  focus, reduced-motion and drawing-alternative probes.

## Required actions before approval

1. Resolve **B1** (raise interactive boundary contrast to ≥3:1) and re-run
   `tests/accessibility.spec.ts` with a non-text-contrast assertion. *(blocking)*
2. Resolve or formally accept **N1** and **N2**, both of which sit on the blocking
   `marketing-responsive` check.
3. Reconcile **N3** and **N4** — either fix the implementation or correct
   `planning/02-visual-direction.md` so its "verifiable constraints" are actually true.
4. Address **N5**/**N6** to make the regression evidence regression-capable.

## Residual risks

No screen-reader, switch, voice or magnification testing was performed; no real-device testing; no
zoom/reflow at 200–400 %; browser coverage is Chromium-only. Data provenance of the numbers shown in
the drawings was spot-checked for internal consistency (12 houses = 7 available / 3 reserved / 2 sold
agrees across home, `/residences` and the empty state) but not audited against
`evidence/content/content-integrity.json` in full.

## Outcome

**Changes required**

The visual thesis, motion discipline and evidence craft are genuinely above reference quality, and
`marketing-visual-thesis` and `marketing-motion-purpose` pass cleanly. Approval is withheld only
because one High finding (B1) sits squarely on the blocking `marketing-accessibility` check, with two
Medium findings on the blocking `marketing-responsive` check. B1 is a one-token fix; on evidence of its
correction plus a response to N1–N3, this build is approvable.
