# P4.3 Asteria normalized frozen-target results

P4.3 re-evaluated the exact first-frozen P4 Asteria implementations through one campaign-owned public HTTPS and Chromium evidence floor. This is an environment-normalized evidence comparison, not a new model benchmark score.

## Immutable historical baseline

| Target | Runtime-reported model | Historical score | Frozen implementation commit |
| --- | --- | ---: | --- |
| Codex | GPT-5 | 53.15 | `a1751e8558beddee8e8c57d2b3f47de86e1c5860` |
| Claude Code | claude-opus-5 | 86.40 | `bff32598806c7ea9b6cd4c2218ee7d5eac2d0816` |

The historical scores remain unchanged. P4.3 did not mutate either target and did not rerun either coding model.

## Final normalized experiment

- GitHub Actions run: `31766968681`
- Campaign commit used by the experiment: `c19dcfd42fb43a00e9793122c1116e236c8d8b36`
- Result: all Codex, Claude Code, and comparison jobs completed successfully.
- Common deployment class: `controlled-preview`
- Public ingress: pinned Cloudflare Quick Tunnel
- TLS: verified TLS 1.3 for both targets
- Browser: Playwright `1.55.0`, Chromium `140.0.7339.16` / build `1187`
- Viewports: 360×800, 768×1024, 1280×800, 1920×1080
- Public surfaces: seven fixture-equivalent routes per target plus a real missing route
- Screenshots: 28 per target

The temporary `trycloudflare.com` URLs were evidence-only endpoints and expired with the workflow jobs. They are not production deployments and must not be used to pass `marketing-production-domain`.

## Artifact provenance

| Artifact | ID | SHA256 digest |
| --- | ---: | --- |
| `p4-3-normalized-codex` | `9206692082` | `ec5f33c1a75c31103832fc321c7d2ee8f752441c40073c0e6d5e5d91ee6f4af0` |
| `p4-3-normalized-claude-code` | `9206706829` | `7c26cb20794140a2e7a9d9c20093b6e1315b949bc77830fd37285d703e1b7893` |
| `p4-3-normalized-comparison` | `9206710306` | `0ba72e49105aed8b141ba3fb7c3d39987d49e22e7c6280d5e6648642cf33c5ae` |

Artifacts retain browser summaries, screenshots, application/tunnel logs, deployment evidence, normalized summaries, and the comparison output.

## Common normalized check matrix

| Check | Codex | Claude Code |
| --- | --- | --- |
| Public HTTPS | pass | pass |
| TLS verified | pass | pass |
| Controlled-preview truth | pass | pass |
| Required surfaces return 2xx/3xx | pass | pass |
| No horizontal overflow | **fail** | pass |
| No target-attributable console errors | pass | **fail** |
| No page errors | pass | pass |
| No target-attributable failed requests | pass | pass |
| No target-attributable HTTP error responses | pass | **fail** |
| Form fields labeled | **fail** | pass |
| 404 SEO truth | **fail** | **fail** |
| Overall normalized floor | **fail** | **fail** |

## Codex findings under the common lab

The frozen Codex implementation was much more observable once the environment asymmetry was removed:

- all seven required surfaces loaded successfully across all four viewports;
- 28 screenshots were captured;
- zero console errors;
- zero page errors;
- zero failed requests;
- zero HTTP 4xx/5xx responses on the tested valid surfaces;
- public HTTPS and TLS 1.3 were verified.

The common browser also revealed concrete product defects that were not merely missing runtime tooling:

1. **Responsive defect:** one viewport produced 11 px of horizontal overflow.
2. **Accessible-name defect:** four contact inputs lack associated labels/ARIA accessible names. Across four viewports this appears as 16 observations of the same field set.
3. **404 SEO defect:** the missing route returned 404 but declared `index,follow,max-image-preview:large` and canonicalised to its `/404` URL, so the error document remained indexable.

This means the original Codex result mixed two causes: environment evidence loss and genuine implementation defects. P4.3 recovers the former without erasing the latter.

## Claude Code findings under the common lab

The frozen Claude implementation preserved strong responsive and form-accessibility behavior:

- zero horizontal overflow across all tested viewports;
- all inspected form fields have accessible labels;
- all seven required surfaces returned success responses;
- zero page errors;
- public HTTPS and TLS 1.3 were verified.

Raw browser output initially contained substantial noise. P4.3 preserves that raw evidence but classifies only transparent, deterministic infrastructure/cancellation cases separately:

- 147 raw console errors total;
- 144 are Cloudflare Quick Tunnel `/cdn-cgi/` email-obfuscation script messages and are recorded as deployment-infrastructure noise;
- 86 raw failed requests are Next.js `_rsc` requests ending `net::ERR_ABORTED` during prefetch/page teardown and are recorded as expected prefetch cancellations;
- none of those 86 are counted as target-attributable failed requests.

Three failures remain target-attributable after that classification:

- `POST /api/events` returned HTTP 429 on `/enquire` at laptop 1280;
- `POST /api/events` returned HTTP 429 on `/residences/ridge-house-01` at wide 1920;
- `POST /api/events` returned HTTP 429 on `/enquire` at wide 1920.

The response resource type was `ping`, so these failures belong to the frozen implementation's analytics/event path rather than navigation availability.

Claude also retains a **404 SEO defect**: the missing route returns 404 and includes `noindex`, but also includes conflicting `index, follow` and canonicalises to the homepage. The error page therefore fails the normalized SEO truth check.

## Interpretation

P4.3 changes the interpretation of the first P4 comparison without changing its scores.

The 33.25-point historical score gap cannot be treated as pure implementation quality because the original Codex runtime lacked browser/public-deployment evidence that P4.3 can now collect successfully. The frozen Codex site is demonstrably reachable, browser-runnable, network-stable on its tested valid routes, and externally probeable when given the common lab.

At the same time, the environment difference was not the whole gap. The normalized lab finds real Codex defects in responsive overflow, form accessible names, and 404 indexing. It also finds real Claude defects in analytics rate limiting and 404 indexing.

The defensible conclusion is therefore:

> **Environment normalization recovers missing observability, but does not collapse implementation differences.**

P4.3 must not be converted into a post-hoc score adjustment. A new benchmark score requires a fresh canonical target run with truthful runtime/model identity, complete product-specific evidence, independent review, and the normal scoring lifecycle.

## Next benchmark move

Asteria has now produced enough measured feedback to justify moving to the second reference-build class instead of repeatedly tuning the marketing-site benchmark. The next campaign should exercise RelayOps, the multi-tenant subscription SaaS fixture, using P4.1/P4.2/P4.3 environment and evidence lessons from the start.
