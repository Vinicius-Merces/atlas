# Asteria — brief synthesis and visual direction

## Sources

- Canonical fixture: `benchmarks/reference-builds/specs/premium-marketing-site.yaml`
- Canonical rubric: `benchmarks/reference-builds/scoring-rubric.yaml`
- Workflow: `.claude/workflows/site-from-brief-delivery.md`
- Capability overlays: Frontend Craft, Web Production Assurance, reference-build benchmark

## Product brief

Asteria is a fictional collection of twelve high-end homes in Serra Clara, near a major urban center. The site must help affluent buyers compare factual property options, understand the place, read useful editorial content, and request an individual visit with low friction and authoritative confirmation.

The conversion is not a button click or client toast. It is a validated, idempotent lead persisted by the server with a stable lead identifier and server-side analytics event.

## Visual thesis

**Measured horizon.** Before copy is read, Asteria should feel quiet, architectural, exact, and rooted in Brazilian landscape—not like a generic black-and-gold luxury template. The composition uses long horizontal rules, large editorial serif type, warm mineral paper, olive landscape tones, and a limited copper accent that behaves like a surveyor's mark.

The signature moments are:

1. a split hero where the building and the unusually large “12” inventory marker share equal authority;
2. the residence ledger, organized like an architect's project register rather than a card grid;
3. abstract plan drawings made only with CSS, used as structural diagrams rather than decorative floating UI.

## Hierarchy and composition

- Primary: the finite collection and its relationship to landscape.
- Secondary: factual residence differences and location context.
- Conversion: one clear visit action in navigation, details, editorial and closing sections.
- Grid: asymmetric two-part editorial layouts; full-width rules separate chapters.
- Mobile: hero copy precedes an immersive image; ledgers shed nonessential columns rather than stacking every datum; forms become single-column with large choice targets.
- Wide screens: content remains anchored within a 1680 px editorial field.

## Typography, media and surfaces

- Editorial serif uses durable system/local fallbacks to avoid a font request and layout shift.
- Sans serif carries navigation, facts, labels and form UI.
- Generated architectural images describe a fictional product and are explicitly labeled illustrative in the footer/terms.
- No autoplay video, WebGL, animation library, glassmorphism, glow, fake awards, testimonials, prices, availability, ratings or invented performance claims.
- Motion is limited to CSS focus/hover feedback and disabled under `prefers-reduced-motion`.

## Stack decision

| Requirement | Choice | Reason |
|---|---|---|
| Multi-route public pages | Server-rendered HTML from Node templates | Crawlable first response; no hydration cost |
| Visual composition | Shared authored CSS | Platform capability is sufficient |
| Interaction | Small progressive-enhancement script | Navigation, analytics and form only |
| Lead authority | Node HTTP API + atomic filesystem persistence | Demonstrates server validation, idempotency and reconciliation without external credentials |
| Analytics | Server JSONL log | Lead success is emitted only after persistence |
| CMS boundary | Structured code-owned content model | Benchmark content is fixed; vendor CMS would add unjustified setup and supply chain |
| Motion/3D | None | The visual thesis is editorial/architectural, not cinematic |

Rejected alternatives: React/Next/Vite, animation packages, WebGL, a hosted CMS, remote font CDNs and a client-only form. They add cost without solving a fixture requirement in this isolated run.

## Content model

- `Residence`: slug, number, name, type, private area, suites, lot, factual summary, features.
- `JournalArticle`: slug, category, title, summary, published date, reading time, structured body.
- Publishing lifecycle: code-owned and reviewed with the run; no editor/draft workflow is claimed.
- Stable slugs and canonical URLs are generated from the same authoritative arrays used for visible content, sitemap and JSON-LD.

## Conversion contract

Valid submissions require name, e-mail, phone, residence interest, budget band and explicit consent. The server normalizes fields, rejects bots through a honeypot, bounds payload size, enforces same-origin mutation, rate-limits per client address, requires an idempotency key and deduplicates a repeated lead identity within 24 hours. It persists before returning success and emits `lead_authoritative_success` only afterward.

The UI preserves data on validation/provider/network failure, exposes associated field errors, disables rapid duplicate submission, and reuses the idempotency key when the network outcome is ambiguous.

## Acceptance and evidence plan

- Routes: home, residences index/detail, location, journal index/article, contact, privacy, terms, robots, sitemap and real 404.
- Browser matrix: 320×720, 390×844, 768×1024, 1366×768, 1920×1080.
- Browser flows: navigation to detail/article/contact; successful lead; validation failure; provider failure; duplicate retry; direct route entry.
- Quality: keyboard/focus, semantic/automated accessibility, reduced motion, overflow, metadata, canonicals, JSON-LD parse/truth, dependency audit, asset sizes and synthetic performance.
- Freeze: copy the first complete implementation and evidence to `evidence/baseline/` before independent findings are remediated.
