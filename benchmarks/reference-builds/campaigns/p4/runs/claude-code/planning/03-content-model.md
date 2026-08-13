# Content Model — Asteria Residences

Capability: `cms-content-modeling`
Workflow: `site-from-brief-delivery` (step 4)

## Decision: repository-authored, schema-governed content with an explicit CMS boundary

The brief has editorial needs (twelve listings whose availability and price band change, a journal,
location content) but no CMS vendor, no editor accounts, and no hosted backend in scope. Adopting a
headless CMS here would be unverifiable theatre: nothing in this run could prove an editor workflow.

Adopted instead: **content is authored as typed modules under `content/`, validated at build time by
Zod schemas, and read only through a repository layer (`lib/content.ts`).** No React component
imports a content file directly and no component contains marketing copy. That makes the
code/content boundary a real, testable seam rather than a promise, and makes the later swap to a
headless CMS a change of one module (`lib/content.ts` source adapter) rather than a rewrite.

Recorded as a deliberate deviation with a migration path, not as an omission.

## Entities

### `Residence` (12 instances, the core entity)

| Field | Type | Notes |
| --- | --- | --- |
| `id` | `A01`–`A12` | stable identifier, never reused |
| `slug` | string | canonical URL segment; changes require a redirect entry |
| `name` | string | e.g. "Residence 04 — Ridge House" |
| `type` | `ridge` \| `terrace` \| `courtyard` | plan family |
| `status` | `available` \| `reserved` \| `sold` | editorial state, drives visible availability |
| `interiorAreaSqm`, `outdoorAreaSqm`, `plotAreaSqm` | number | tabular, comparable |
| `bedrooms`, `bathrooms`, `levels`, `parking` | number | |
| `orientation` | `N`\|`NE`\|`E`\|`SE`\|`S`\|`SW`\|`W`\|`NW` | drives the orientation rose drawing |
| `aspect` | string | short factual sentence |
| `elevationM` | number | metres above the valley datum; pegs the plot on the ridge section |
| `plotX`, `plotY` | number | normalised site-plan coordinates; drive the constellation |
| `priceBandEur` | `{ from, to }` | band, not a fake exact figure |
| `deliveryQuarter` | `2027-Q2` etc. | |
| `energyRating` | string | |
| `summary` | string | ≤ 220 chars |
| `narrative` | string[] | paragraphs, plain text, no embedded markup |
| `features` | `{ group, items[] }[]` | grouped specification |
| `materials` | `{ name, hex, application }[]` | drives the swatch tiles |
| `plan` | `{ level, rooms[{name, areaSqm}] }[]` | drives the floor-plan drawing and the schedule of areas |

### `District` (location surface, 4 instances)

`id`, `slug`, `name`, `distanceKm`, `travelMinutes`, `mode`, `summary`, `narrative[]`, `highlights[]`.
Rendered as in-page anchored sections with an internal contents nav.

### `JournalEntry` (editorial model, 5 instances)

`slug`, `title`, `deck`, `kicker`, `publishedAt`, `updatedAt`, `author {name, role}`, `readingMinutes`,
`tags[]`, `body[]` (typed blocks: `paragraph` | `heading` | `list` | `pullquote` | `figure` |
`dataTable`), `relatedResidences[]`, `relatedDistricts[]`, `status` (`draft` | `published`).
Unknown block types render as nothing rather than throwing — the rendering contract is total.

### `LegalDocument` (3 instances: privacy, terms, cookie/contact basics)

`slug`, `title`, `effectiveDate`, `body[]` (same block union), `noindex` flag.

### `SiteSettings`

Organisation identity, contact points, sales office address, geo coordinates, canonical origin,
default metadata, and the `verified` flag that gates which claims may appear in structured data.

## Editorial state and permissions

- `status: draft` entries are excluded from listings, from the sitemap, and from static generation;
  requesting a draft slug returns 404 in production.
- `status` on a residence (`available` / `reserved` / `sold`) never removes the page — a sold
  residence keeps its URL and gains an availability notice, so links and search results do not rot.
- No public write access to content. The only public mutation on the site is the lead endpoint.

## Localisation

Single locale (`en-GB`) declared explicitly in `<html lang>`, in metadata, and in structured data.
Fields are locale-scalar today; the migration note records that localisation would move to
`Record<Locale, T>` on text fields with `en-GB` fallback. Declared rather than faked.

## Media

No uploaded media. Every drawing is derived deterministically from residence fields by
`lib/drawings/*`, so media cannot drift from the data. This removes the upload/storage lifecycle from
scope, which is why `file-upload-storage-design` is *not* routed (see `06-capability-routing.md`).

## SEO fields

Editors supply `title`, `summary`/`deck`, and nothing else SEO-specific. Canonical URLs, OpenGraph
titles, and structured data are **derived** from authoritative fields so an editor cannot publish a
description that contradicts the visible page. Only `LegalDocument.noindex` is an explicit editorial
control.

## Frontend rendering contract

- Optional fields render as omission, never as "—" placeholder noise, except in comparison tables
  where a `—` with `aria-label="not applicable"` preserves column alignment.
- Long content: narrative paragraphs are capped by measure, not truncated. `features` groups wrap.
- The block renderer is exhaustive over the union and returns `null` for unknown kinds.
- Every list surface has a real empty state (no residences match a filter → a stated message plus a
  reset control), exercised in evidence.

## Migration plan (code → headless CMS)

1. Zod schemas in `content/schema.ts` become the CMS type definitions (1:1 field mapping).
2. `lib/content.ts` gains a source adapter; the module's exported functions are the stable contract.
3. `id` fields become CMS document IDs; `slug` history moves into a redirect collection.
4. Draft/preview moves from the `status` field to CMS preview tokens behind an authenticated route.

## Validation

`npm run validate:content` parses every content module through its schema and additionally asserts:
unique ids and slugs, twelve residences, plot coordinates inside bounds, price band ordering,
`sum(plan rooms) ≈ interiorArea` within tolerance, and no `lorem ipsum` substring anywhere in
content. Result recorded in the evidence ledger.
