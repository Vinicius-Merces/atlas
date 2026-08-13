# Frontend Stack Selection — Asteria Residences

Capability: `frontend-stack-selection`
Workflow: `site-from-brief-delivery` (step 2)

## Existing stack assessment

Greenfield. No existing framework, design system, component library, or animation stack to preserve.
The repository is the ATLAS framework itself; the reference build is self-contained under
`benchmarks/reference-builds/campaigns/p4/runs/claude-code/site/` and shares no dependencies with it.

## Requirements → tool matrix

| Requirement | Chosen tool | Why the smaller option was rejected / not needed |
| --- | --- | --- |
| Public routes, static generation of 12+ residence pages, per-route metadata, `robots`, `sitemap` | **Next.js 16 App Router** | A hand-rolled static build could render pages, but the fixture requires an authoritative server-side lead mutation *and* per-route metadata/canonical control on the same origin. Next gives both without a second service. |
| Authoritative lead mutation | **Next Route Handler (`app/api/...`) on Node runtime** | A server action would work, but an explicit HTTP endpoint is directly inspectable in browser-network evidence and testable with `curl`, which the benchmark requires. |
| Lead persistence | **SQLite via `node:sqlite`** (Node 22 built-in) | Rejected `better-sqlite3` (native rebuild, supply-chain surface) and rejected a JSON file (no atomicity, no unique constraint, cannot prove duplicate protection). The built-in module adds **zero** dependencies and gives real transactions and a real `UNIQUE` index. |
| Input validation | **Zod** | Hand-written validators would duplicate the content schemas; Zod is already required for the content model, so it is one dependency serving two needs. |
| Styling / design tokens | **Plain CSS: one token layer + CSS Modules** | Rejected Tailwind: the visual thesis is a bespoke drawing-sheet system with hairline rules and a margin grid, and utility classes would both hide that system and import a default aesthetic the direction explicitly rejects. Rejected CSS-in-JS: runtime cost with no benefit here. |
| Typography | **`@fontsource-variable/fraunces`, `@fontsource-variable/newsreader`, `@fontsource/ibm-plex-mono`** | Self-hosted, no third-party font origin, no render-blocking external request, no privacy exposure, and it works in an allowlisted-egress environment. |
| Motion | **Platform CSS only** (one `stroke-dashoffset` transition + colour/rule transitions) | Rejected Motion and GSAP outright. The direction has exactly one narrative animation and no scroll choreography, timelines, shared-layout transitions or gestures. Adding an animation library for a single 900ms stroke would be trend-driven weight. |
| 3D | **None** | Rejected Three.js / R3F. The ridge is communicated by a measured 2D section, which is *more* legible and truthful than a decorative 3D massing model and costs no WebGL budget on mobile. Recorded as a deliberate rejection, not an oversight. |
| Accessible primitives | **Native HTML** (`<details>`, `<fieldset>`, `<table>`, `<dialog>`-free) | Rejected Radix / Base UI / React Aria: the site has no menu, combobox, popover, or focus-trapped overlay. Every interactive control maps to a native element, so a primitive library would add bundle and indirection for zero behaviour. |
| Charts / dataviz | **Hand-authored SVG** | No chart library. The drawings are information design specific to this product; a generic chart library cannot draw a ridge section. |
| Tests | **`node:test`** (built-in) for unit/contract, **Playwright** for browser evidence | Rejected Jest/Vitest: `node:test` is sufficient and dependency-free. Playwright is required by the browser-reality axis and Chromium is preinstalled. |
| Accessibility scanning | **`@axe-core/playwright`** | Required for automated WCAG evidence across every route; no lighter equivalent. |
| Performance measurement | **Playwright/CDP metrics + byte-budget script over the built output** | Rejected a Lighthouse dependency: the value needed is field-representative mobile timings and transfer budgets, both obtainable from CDP on the emulated mobile profile, with the raw numbers recorded. |

## Selected stack (final)

**Runtime dependencies:** `next`, `react`, `react-dom`, `zod`, three `@fontsource*` packages.
**Dev dependencies:** `typescript`, `@types/*`, `@playwright/test`, `@axe-core/playwright`.

That is the whole list. Nothing is installed for the look of the dependency graph.

## Bundle / runtime / accessibility implications

- All twelve residence pages, the home page, location, journal, and legal pages are **statically
  generated**; only `/enquire` ships meaningful client JavaScript (the form's progressive
  enhancement) and only the home/residence pages ship the ~1.5 KB plot cross-highlight script.
- The form **works without JavaScript**: it is a real `<form method="post">` posting to a route
  handler that content-negotiates and returns a server-rendered confirmation page. Client JS upgrades
  it to inline validation and an ARIA-live status region. This is the accessibility and
  failure-resilience floor, not a nice-to-have.
- No web fonts from a third-party origin; two preloaded woff2 subsets above the fold.
- Zero animation library means reduced-motion support is a single media query with no library
  configuration to get wrong.

## Escalation

No WebGL, no persistent animation loop, no cross-project dependency, no substantial client
JavaScript. Architecture/performance escalation is **not** triggered. Recorded so the absence is a
decision rather than a gap.

## Supply-chain note

Every runtime dependency is a first-party-maintained or widely-audited package; the total direct
dependency count is 7. `npm audit` output and a full dependency inventory are recorded under
`evidence/supply-chain/`.
