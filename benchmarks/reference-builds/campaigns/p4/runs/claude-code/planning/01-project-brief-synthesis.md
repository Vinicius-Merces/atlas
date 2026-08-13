# Project Brief Synthesis — Asteria Residences

Capability: `project-brief-synthesis`
Workflow: `site-from-brief-delivery` (step 1)
Run: P4 / target `claude-code` / model `claude-opus-5`

## Sources

- `benchmarks/reference-builds/specs/premium-marketing-site.yaml` (canonical fixture, sha256 `e57da062…62947`)
- `benchmarks/reference-builds/campaigns/p4/runtime-packets/claude-code-asteria.md`
- `benchmarks/reference-builds/campaigns/p4/campaign.yaml`
- `.claude/workflows/site-from-brief-delivery.md`
- `.claude/rules/global.md`

No prior Asteria implementation, evidence, or result from any other campaign branch was read.

## Product and current state

Asteria Residences is a fictional boutique development of **twelve** high-end homes near a major
urban center. Nothing exists yet: this is a greenfield public marketing site. The homes are sold
**off-plan** — a decision derived from the brief ("a boutique residential development", "concrete
property information", no existing asset library) and it drives the whole content and visual model:
there are no photographs of a building that is not built, so the site must be honest about that
rather than dress itself in generic stock luxury imagery.

## Audience and job to be done

Affluent buyers (and their brokers) comparing premium properties, on mobile as often as desktop.
Their jobs, in order:

1. **Decide quickly whether this is credible.** Who is building it, where, when, and at what level.
2. **Get concrete, comparable facts.** Area, orientation, levels, bedrooms, outdoor area, parking,
   delivery date, price band, availability — per residence, in a form they can compare.
3. **Understand the place, not just the building.** What the ridge, the neighbourhood, and the
   commute actually are.
4. **Talk to a person with low friction and no spam anxiety.** A visit request that is clearly
   received, referenced, and answered.

They are hostile to: fake urgency, unverifiable superlatives, autoplaying video, mystery pricing,
and forms that swallow their data.

## Conversion / information objective

Primary conversion: **a qualified visit request** — a lead that reaches an authoritative server-side
record with a human-quotable reference code, routed to the sales broker. Qualification fields
(residence of interest, buying timeframe, purchase context) exist so the broker call is useful, not
so the form is longer.

Secondary objectives: residence-detail depth reached, location section read, journal entry read.
These are measured as server-side funnel events, not as vanity page views.

## Content authority

Editorial content (residences, location districts, journal entries, legal pages) must be
maintainable by a small marketing team without a frontend release *in the target end-state*, but the
brief has no CMS vendor, no editor identities, and no hosting for one. Decision recorded in
`03-content-model.md`: **typed, schema-validated content modules in the repository as the
authoritative source, with an explicit, documented CMS boundary and migration path.** The boundary is
real (all content passes a runtime schema and no component reads free-form copy), not aspirational.

## Constraints carried from the fixture

- No copying an existing luxury real-estate site; no lorem ipsum in final content.
- No autoplay background video carrying the value proposition.
- Motion/3D must be justified by the visual thesis and must respect reduced motion and mobile perf.
- Public production routes need explicit crawl/index/canonical behaviour.
- A client-side success toast is **not** proof a lead landed.

## Environment constraints (recorded before implementation)

Network egress in this run is allowlisted to the npm registry and `github.com`. Vercel, Netlify,
Cloudflare APIs and every tunnel provider tested are unreachable, and the campaign forbids pushing
any branch other than `bench/p4-asteria-claude-code`, which rules out a GitHub Pages publish branch
(and GitHub Pages could not host the authoritative lead mutation anyway). Consequence, decided
*before* building rather than after scoring: the site is built and validated as a **real production
build served over HTTPS on a real hostname in this environment**, and
`marketing-production-domain` is reported honestly as not fully verified. See
`evidence/production/deployment-constraint.md`. No check will be upgraded to compensate.

## Open risks

| Risk | Handling |
| --- | --- |
| Off-plan project has no photography | Visual thesis is built on drawings, not on substitute stock photos (see `02-visual-direction.md`) |
| No public hosting | Production-parity local HTTPS deployment; affected check reported below `pass` |
| No third-party analytics reachable | First-party server-side conversion events, deduplicated by lead reference |
| Lead "success" could be faked by UI | Reference code issued by the server, verifiable through an authenticated read endpoint used in evidence |

## Next actions

1. Visual direction (`interface-visual-direction`) → `02-visual-direction.md`
2. Content model (`cms-content-modeling`) → `03-content-model.md`
3. Stack selection (`frontend-stack-selection`) → `04-stack-selection.md`
4. Lead mutation contract (`form-mutation-design`) → `05-lead-mutation-contract.md`
5. Capability routing decision record → `06-capability-routing.md`

## Validation status

Brief synthesized from the canonical fixture only. Every claim above is traceable to the fixture,
the runtime packet, or a recorded environment probe. Nothing validated by execution yet.
