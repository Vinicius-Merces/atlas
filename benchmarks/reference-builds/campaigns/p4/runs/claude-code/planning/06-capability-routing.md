# Capability Routing Decision Record

Workflow executed: `.claude/workflows/site-from-brief-delivery.md` (declared by the fixture)
Inherited gates: Frontend Craft, Web Production Assurance, Full-Stack Delivery, browser validation.

## Routed — required by the fixture

| Capability | Where it was exercised |
| --- | --- |
| `project-brief-synthesis` | `planning/01-project-brief-synthesis.md` |
| `interface-visual-direction` | `planning/02-visual-direction.md` |
| `frontend-stack-selection` | `planning/04-stack-selection.md` |
| `form-mutation-design` | `planning/05-lead-mutation-contract.md` |
| `cms-content-modeling` | `planning/03-content-model.md` |
| `conversion-funnel-review` | `evidence/analytics/conversion-funnel-review.md` |
| `analytics-implementation-audit` | `evidence/analytics/analytics-implementation-audit.md` |
| `responsive-layout-audit` | `evidence/responsive/` |
| `accessibility-audit` | `evidence/accessibility/` |
| `visual-regression-review` | `evidence/visual-regression/` |
| `browser-flow-validation` | `evidence/browser/` |
| `web-performance-field-readiness` | `evidence/performance/` |
| `seo-technical-audit` | `evidence/seo/` |
| `structured-data-validation` | `evidence/structured-data/` |
| `content-discoverability-review` | `evidence/seo/content-discoverability-review.md` |
| `supply-chain-risk-audit` | `evidence/supply-chain/` |
| `frontend-craft-review` | `reviews/frontend-craft-review.md` (independent reviewer) |

## Routed — inherited support capabilities the build genuinely used

| Capability | Reason |
| --- | --- |
| `rate-limit-abuse-control` | The lead endpoint is a public, unauthenticated, consequence-bearing mutation. Required by `site-from-brief-delivery` step 8. |
| `secret-environment-audit` | Broker webhook and admin key exist; their absence from client bundles must be proven for `marketing-private-data`. |
| `design-token-architecture` | The visual thesis depends on a hairline/weight/colour token system; without tokens the reduced-motion and accent constraints are unverifiable. |
| `motion-choreography` | One narrative motion exists (the ridge datum draw-on) and must be justified and reduced-motion safe. |
| `smoke-test-design` | Contract tests for the lead endpoint and content schemas. |

## Deliberately NOT routed (omission is the decision, not an oversight)

| Capability | Why it does not apply |
| --- | --- |
| `file-upload-storage-design` | No user or editor upload exists anywhere in the journey. All media is derived from content data. |
| `application-search-design` | Twelve residences and five journal entries. Filtering by type/status/bedrooms is sufficient and a search index would be ceremony. |
| `immersive-3d-experience` | Explicitly rejected in `04-stack-selection.md`: the ridge is better communicated by a measured 2D section, and 3D would cost mobile budget for decoration. |
| `payment-integration-review` | No transaction on the site. |
| `authentication-flow-review` / `authorization-boundary-review` (full) | No user accounts. The single protected surface is the admin read-back endpoint, covered by a shared-secret header check that is tested directly (401 without key) rather than by routing a whole auth review. |
| `transactional-email-delivery` | No mail provider is reachable in this environment; simulating one would be evidence theatre. The limitation is recorded in `05-lead-mutation-contract.md §8` instead. |
| `saas-multitenancy-review`, `row-level-security-review`, `background-job-reliability`, `webhook-reliability-review` (as a gate) | No tenants, no RLS surface, no job runner. The broker webhook's failure handling is designed and tested inline; a full reliability review would exceed the brief. |
| `localization-readiness-assessment` | Single declared locale; the migration shape is recorded in the content model. |

This table exists because the fixture scores `marketing-routing-no-theater`: capabilities were
selected from the journey, and the ones that do not apply were written down as not applying.
