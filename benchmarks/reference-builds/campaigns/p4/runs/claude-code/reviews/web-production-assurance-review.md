# Web Production Assurance & Reference-Build Benchmark Review — Asteria Residences (P4)

- **Reviewer:** Independent Web Production Assurance and benchmark reviewer (claude-code subagent, did not implement)
- **Date:** 2026-08-13
- **Run:** `p4-live-reference-build-campaign` / target `claude-code`
- **Branch:** `bench/p4-asteria-claude-code`
- **Commit under review:** `bff32598806c7ea9b6cd4c2218ee7d5eac2d0816` ("bench(p4): Asteria Residences reference build — claude-code target implementation and evidence")
- **Campaign base commit:** `3ccdf6e6209c3aea949e62226af1cb6b35167487` (verified to be an ancestor of the run head)
- **Fixture:** `benchmarks/reference-builds/specs/premium-marketing-site.yaml`, sha256 `e57da062…62947` — **recomputed and matches** `run-manifest.json`
- **Rubric:** `benchmarks/reference-builds/scoring-rubric.yaml`, sha256 `6463ae7f…1b56b31` — **recomputed and matches**
- **Gates applied:** `.claude/reviews/web-production-assurance-review.md`, `.claude/reviews/reference-build-benchmark-review.md`, `.claude/reviews/full-stack-delivery-review.md`
- **Independence:** I did not implement this build, did not author any of its evidence, and inspected no other `bench/p4-asteria-*` branch or history.

## Method — what I re-ran myself

Everything below marked **[re-ran]** was executed by me against the live production build during this review, not read out of the committed JSON.

- **[re-ran]** Lead submissions by `curl` against `:3100` (valid, invalid, injected fields, 6-way concurrent, case/whitespace-variant email), authenticated read-back, `_stats` parity.
- **[re-ran]** Forced-failure instances `:3102` (store) and `:3103` (provider), and the production-default rate limiter on `:3101`.
- **[re-ran]** Full Playwright suites: `browser-flows.spec.ts` (13 passed), `accessibility.spec.ts` (21 passed), `responsive.spec.ts` (40 passed) — 74/74, all reproduced.
- **[re-ran]** Collectors `collect-seo.mjs`, `collect-structured-data.mjs`, `collect-security.mjs`, `validate-content.mjs` — all exit 0, "no problems found", reproducing the committed reports.
- **[re-ran]** `npm audit --json`, lockfile registry/integrity/install-script analysis.
- **[re-ran]** Live HTTP inspection of `robots.txt`, `sitemap.xml`, canonicals, robots metas, security headers, redirects, 404 status, no-JS native form POST.
- **[re-ran]** Egress probes to Vercel / Netlify / Cloudflare / trycloudflare / npm / GitHub to test the deployment-constraint claim.
- **[re-ran]** `grep` of `.next/static` for the admin key, env-var names and DB paths.

The working tree was restored to `HEAD` after my re-runs; the only untracked additions are this review and the parallel Frontend Craft review.

---

## Blocking checks — explicit statement

| Blocking check | My verdict | Basis |
| --- | --- | --- |
| `marketing-lead-authoritative` | **pass** | I submitted a lead myself and read it back through the authenticated endpoint; duplicate protection survived every attack I made on it. |
| `marketing-responsive` | **pass on the evidence in my scope** (40/40 re-run); *defer* to the independent Frontend Craft reviewer, who scored it **partial** | Not my axis; I did not override a peer reviewer's rendered-craft judgement. |
| `marketing-accessibility` | **pass on the evidence in my scope** (21/21 re-run, axe zero violations on 14 routes + 2 form states); *defer* to Frontend Craft reviewer, who scored it **partial** | Same. |
| `marketing-browser-primary-flow` | **pass** | Re-ran; the flow asserts an authoritative server read-back, not a UI toast. |
| `marketing-production-domain` | **partial** — honestly reported, correctly scored below pass | I independently confirmed no public deployment exists and cannot exist here. |
| `marketing-seo-indexing` | **partial** | Live crawl signals are correct on all 2xx routes, but 404 responses emit two conflicting `robots` metas and canonicalise to the homepage, and the SEO collector cannot see either defect. |

**Consequence:** at least two blocking checks (`marketing-production-domain`, `marketing-seo-indexing`) are not `pass`. Under `scoring-rubric.yaml` → `claim_policy.require_no_blockers` and rule "Any blocking check not marked pass blocks the run regardless of score", **this run is blocked and non-claimable** irrespective of aggregate score. The implementation's own `evidence/production/deployment-constraint.md` reaches the same conclusion unprompted, which I regard as a mark of integrity rather than a defect.

---

## Per-check verdicts

### Axis: `security_isolation` (weight 5)

**`marketing-form-security` — pass** *(re-verified)*

- Server-side validation is authoritative: my malformed submission was rejected `422` with per-field messages even though the client form was bypassed entirely (`curl`).
- Media-type and payload bounds enforced live: `text/plain` → `415`, 20 KB body → `413`, broken JSON → `400`.
- Abuse controls proven on the **production-default** instance `:3101`: 5 accepted, then `429` with `Retry-After: 120` — I ran this myself, it is not a replay of committed evidence. Honeypot returns a decoy `200` with `AST-000000` and writes nothing; a sub-2s submit is rejected `429`.
- Provider/secret boundary: the broker webhook and admin key are read from `process.env` in server-only modules; the admin endpoint uses `timingSafeEqual` with a length guard.
- Live headers on every response I fetched: `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options: DENY`, `Referrer-Policy`, `Permissions-Policy`, no `X-Powered-By`.
- Caveats recorded as findings, not verdict-changing: CSP allows `script-src 'unsafe-inline'`; no HSTS (unverifiable without TLS).

**`marketing-private-data` — pass** *(re-verified)*

- I grepped `.next/static` (36 files, 19 JS/CSS/map) myself for `bench-p4-admin-key-3f9c2a71`, `ASTERIA_ADMIN_KEY`, `ASTERIA_IP_SALT`, `ASTERIA_DB_PATH`, `asteria-local-salt` and for any `ASTERIA_*` token: **zero hits**. No `NEXT_PUBLIC_*` variable exists in the codebase.
- Served HTML references only `https://asteria-residences.example` and `https://schema.org`; no third-party origin, script, font or pixel.
- Lead data is unreadable without the key: `GET /api/visit-requests/<ref>` and `/_stats` return `401` with no key and with a wrong key; `/data/*.db`, `/.env*`, `/.next/server/...` return 404.
- `collect-security.mjs` searches for the **actual secret value**, not a label — the marker list is a real regex set. This is honest evidence, not a checklist.

### Axis: `failure_resilience` (weight 8)

**`marketing-provider-failure` — partial** *(re-verified; downgraded on a truthfulness ground, not a behavioural one)*

- Behaviour is correct and I confirmed it live. On `:3103` a submission returns `201` with `notification: "failed"`; the authenticated read-back shows `status: received`, `notification_status: failed`, `notification_error: simulated_broker_failure`, `notification_attempts: 1`; `_stats` = 1 lead / 1 conversion event. No silent loss. On `:3102` the store failure returns `503`, the copy says "was NOT recorded. Nothing has been sent", and `_stats` stays at 0/0 — a failure is never dressed as success.
- **However**, both the API message and `/enquire/received` tell the visitor the hand-off "is being retried automatically", and `planning/05-lead-mutation-contract.md §8` states "the broker webhook retry is in-process with bounded attempts". **No retry exists.** `notifyBroker` has exactly one call site (`app/api/visit-requests/route.ts:186`), performs one attempt, and there is no queue, interval, cron or replay endpoint anywhere in the site (`background-job-reliability` is explicitly *not routed* in `planning/06-capability-routing.md`, consistently with the code but inconsistently with the copy).
- The recovery path that *does* exist — durable lead, honest degraded status, reference code, telephone fallback, admin read-back — is good. The claimed automatic recovery path does not exist. A visitor is being told something untrue about a consequential state.

**`marketing-duplicate-submit` — pass** *(re-verified, attacked)*

- Idempotency-key replay → same reference, `duplicate: true`, no second row.
- **6 concurrent POSTs with six distinct idempotency keys**, same email + residence: 1 created, 5 duplicates, all returning the same reference `AST-MYNH3X90`; `_stats` incremented by exactly 1 lead and 1 event. The dedupe is enforced by SQLite `UNIQUE` constraints inside a `BEGIN IMMEDIATE` transaction, so it is a real race guard, not a read-then-write check.
- Normalisation cannot be evaded: `"  RACE.Tester@Example.com "` was caught as the same-day duplicate of `race.tester@example.com`.
- Client-supplied `reference`, `status`, `notification_status` fields are ignored — my injection attempt received a fresh server-issued reference (`AST-ZSD00M89`).

**`marketing-degraded-assets` — pass** *(re-verified)*

- The Playwright case aborts every `woff/woff2/ttf/png/jpg/jpeg/webp/avif/gif` request and then completes home → residences → enquire with real assertions on headings, links and form fields, asserting `pageErrors === []`. It reproduced for me.
- Independently: the site is genuinely server-rendered (5.7k–7.9k chars of text in the raw HTML per route), the enquire form has `action="/api/visit-requests" method="post"`, and a raw urlencoded POST returned `303` to `/enquire/received?ref=AST-JAFX1RB2` — the journey survives with no JavaScript at all.

### Axis: `browser_reality` (weight 10)

**`marketing-browser-primary-flow` — pass (BLOCKING)** *(re-ran)*

Home → primary nav → 12 residence cards asserted → detail (`404 m²`, spec table) → CTA carrying `?residence=A04` → pre-selected field asserted → submit → `role=status` "Recorded" → reference matched against `/^AST-[0-9A-Z]{8}$/` → **authenticated read-back asserting email, `residence_id === "A04"` and `status === "received"`**. This is the assertion the fixture's prohibited-shortcut clause demands, and it is present.

**`marketing-browser-negative-flow` — pass** *(re-ran)*

Empty submit (field errors, `aria-invalid`, `aria-describedby`, focus moved), malformed email + missing consent, duplicate resubmission with before/after `_stats` deltas, store failure on `:3102` (asserts the success string is *absent* and the visitor's input survives), provider failure on `:3103` (asserts the stored record, not the UI).

**`marketing-browser-console-network` — pass** *(re-ran)*

Diagnostics are collected per journey and asserted to be empty for `pageErrors`, `consoleErrors`, `failedRequests` and `badResponses`. There is one carve-out — `_rsc=` prefetches aborted with `net::ERR_ABORTED` are bucketed as `cancelledPrefetches` — which is a genuine Next.js navigation artefact, is narrowly scoped to that exact URL+error pair, and is retained in the evidence rather than discarded. I accept it; I note it as the one place where a weakening would be easy to hide.

### Axis: `production_readiness` (weight 12)

**`marketing-production-domain` — partial (BLOCKING), honestly reported** *(re-verified)*

I probed egress myself: `api.vercel.com`, `api.netlify.com`, `api.cloudflare.com`, `api.trycloudflare.com`, `loca.lt`-class tunnels all return curl exit 000 (no route); only `registry.npmjs.org` and `api.github.com` return 200. `https://asteria-residences.example/` does not resolve. There is no public deployment, no DNS, no TLS, no CDN — and the run does not claim one anywhere. `evidence/production/deployment-constraint.md` states precisely what was and was not verified, states that `partial` (not `pass`) is the score, and states that the run is therefore blocked. `run-manifest.json` `notes` says the same. **This is the correct and honest handling**; the only quibble is that the constraint doc records a `403 Host not in allowlist` for trycloudflare where I now observe a plain 000, an immaterial difference in proxy state.

One point of discipline worth crediting: no other check in the tree cites a deployment that did not happen, and no score is inflated to compensate.

**`marketing-seo-indexing` — partial (BLOCKING)** *(re-verified against live responses)*

Verified correct by me, on the wire:
- `robots.txt` 200, `Allow: /`, `Disallow: /api/`, `Disallow: /enquire/received`, `Disallow: /residences?`, sitemap declared.
- `sitemap.xml` 200 with exactly 25 URLs = 5 static + 12 residences + 5 published journal entries + 3 legal; the draft entry `material-samples-autumn` is absent (and returns 404 directly); `/enquire/received` is absent.
- Self-referential canonicals on all 13 indexable routes, exactly matching `https://asteria-residences.example<path>`; `lang="en-GB"`; one `<h1>` per route; OG/Twitter metadata present; filtered `/residences?status=sold` correctly canonicalises to `/residences`.
- `/enquire/received` is `noindex, follow` and excluded from the sitemap; `/residences/` and `/enquire/` 308 to the canonical form; `/no-such-page` and `/residences/no-such-house` return a genuine `404`.
- All 12 residence detail pages are linked from `/residences`; content is in the server response, not hydration-only.

**Defect:** on 404 responses the document contains **two conflicting robots directives** —
```
<meta name="robots" content="noindex"/>
<meta name="robots" content="index, follow"/>
```
— and a `<link rel="canonical" href="https://asteria-residences.example">` pointing the error document at the homepage. Root cause: `app/layout.tsx` sets a global `robots: { index: true, follow: true }` and `alternates.canonical = "/"`, which the framework 404 render inherits alongside Next's own injected `noindex`. In practice the restrictive directive wins and the 404 status makes it moot, but "conflicting crawl signals" and "canonicalisation away from intended content" are exactly the failure modes this gate names, and a soft-404 canonical to the homepage is a real (if bounded) risk.

**The evidence understates this.** `evidence/seo/seo-audit.json` reports `"problems": []`. It cannot report the conflict because `collect-seo.mjs` extracts metadata with a first-match regex (`pick`), so the second `robots` tag is invisible, and it `continue`s past every metadata assertion for routes expected to be `404`, so the homepage canonical on an error document is never checked. This is a collector blind spot rather than a fabrication — but it means a green report is being cited for a property that was not actually tested.

**`marketing-structured-data` — pass** *(re-verified against the visible pages)*

I fetched three residence pages and parsed their JSON-LD myself:
- `ridge-house-01` (visible status **Sold**): `SingleFamilyResidence` with **no `offers` and no `Offer` node**.
- `courtyard-house-12` (visible status **Reserved**): **no `offers`**.
- `ridge-house-04` (visible status **Available**): publishes `Offer` with `priceSpecification` `minPrice 2900000` / `maxPrice 3180000` EUR — and the page visibly reads **€2.90M–€3.18M**. `availability: PreOrder` is the truthful value for an off-plan sale.
- Entity graph is coherent (`@id`-linked `RealEstateAgent`, `Place`, `WebSite`, `BreadcrumbList`); floor/lot areas in the graph appear verbatim on the page; no invented ratings, reviews or aggregate ratings anywhere.

`collect-structured-data.mjs` does not merely validate syntax — it asserts each value against the rendered text and *explicitly fails* if a sold/reserved residence publishes an Offer. That is the right test and it is real. Limitation to record: no external Rich-Results/schema validator was run (no egress), so "syntactically valid" rests on `JSON.parse` plus type checks.

**`marketing-performance` — pass, with a truthfulness note** *(evidence read, methodology audited; not re-measured)*

- Method is legitimate: production build, Playwright/CDP, 390×844 @3x, 4× CPU throttle, 1.6 Mbps/750 Kbps/150 ms, transfer sizes taken from CDP `encodedDataLength` (post-compression wire bytes, not decompressed). The loopback-emulation caveat is stated in the artefact itself.
- Results across six routes: 309–321 KB total, 139–140 KB script, LCP 564–828 ms, CLS 0–0.056, DCL 573–846 ms, 26–32 requests. Comfortably inside every timing budget.
- **On the 321 KB vs 320 KB question:** the overshoot on `/residences/ridge-house-04` is *retained* in `performance.json` → `"problems": ["/residences/ridge-house-04: 321 KB total > 320 KB budget"]`, and `collect-performance.mjs` `process.exit(1)`s on it. A budget tuned after measurement would have been set at 330 and the artefact would be clean. The behaviour here is the opposite of budget-tuning, and I credit it.
- **What I cannot verify:** the comment "Budgets, declared before measurement" is unfalsifiable from a single squashed commit — there is no pre-measurement artefact declaring 320/190/130/40 and no planning document states those numbers. The band is also uncomfortably tight against the observed range. I record this as an ordering claim that is *unproven but non-self-serving*, and I do not treat it as dishonesty.

**`marketing-analytics` — pass** *(re-verified by experiment)*

- **A client cannot emit a conversion event.** I posted `{"name":"conversion.visit_request.submitted","sessionId":"attacker","subject":"A01"}` to `/api/events`: **`422`**. A legitimate funnel step (`enquire_opened`) returned `204`. The allow-list in `app/api/events/route.ts` contains only the two non-conversion steps.
- **Lead count == conversion event count.** After my own three submissions on `:3100`, `/_stats` returned `{"visitRequests":3,"conversionEvents":3}`. On `:3103` after one provider-failure lead: `1/1`. On `:3102` after a store failure: `0/0` — the event insert is inside the transaction that rolled back, so no orphan conversion exists.
- The conversion row is written server-side in the *same* SQLite transaction as the lead, with a `UNIQUE` dedupe key on the reference. This is the architecturally correct answer to the fixture's "a toast is not proof" constraint, and the analytics review document describes it accurately.
- No third-party analytics, tag manager or pixel; `connect-src 'self'` in CSP; the privacy notice's no-third-party-tracking promise is therefore true.

### Supply chain

**Assessed: pass** *(re-verified)*

- 13 direct (7 runtime: `next`, `react`, `react-dom`, `zod`, three self-hosted `@fontsource*` packages), 93 packages in the resolved tree.
- I re-ran `npm audit --json`: `{info:0, low:0, moderate:0, high:0, critical:0}`.
- I re-parsed `package-lock.json` (v3) myself: **0 packages resolving outside `registry.npmjs.org`, 0 packages missing an integrity hash, exactly 1 package with an install script (`fsevents`, a darwin-only optional dep that never executes here)**.
- No lifecycle script of the project's own, no vendored binary, no container base, no CI action introduced. The lead store uses built-in `node:sqlite` rather than a native addon, genuinely removing a compiled dependency from the surface.
- Note: `transitivePackages` lists many `…@undefined` entries (uninstalled optional platform binaries). Cosmetic, but it makes the "93 transitive packages" figure look larger than the real installed set.

### Independent review axis

- **`marketing-review-frontend` — present.** `reviews/frontend-craft-review.md` was authored during this session by a separate non-implementing claude-code subagent; it scores `marketing-responsive`, `marketing-accessibility` and `marketing-visual-regression` as **partial**. I did not co-author it and do not adopt or overturn its conclusions; I note that it independently constrains two further blocking checks.
- **`marketing-review-production` — this record.**

---

## Benchmark-truthfulness sweep

**What is genuinely honest here** (stated first, because it is the majority of the picture):

- The blocking check that could not be satisfied is reported as failing, with the failure mechanism, the attempted workarounds, and the scoring consequence spelled out — before anyone asked.
- The one performance budget breach is retained and makes the collector exit non-zero.
- Every collector fetches live responses and `process.exit(1)`s on any problem; none of them "assert nothing". The Playwright specs assert outcomes (row deltas, `_stats` parity, authoritative read-back, axe violation lists, overflow/tap-target/measure numbers), not merely that a click happened.
- I reproduced 74/74 tests and 4/4 collectors from a clean tree. Nothing in the evidence tree is unreproducible.
- The test-environment deviation (rate capacity raised to 50 on `:3100`) is disclosed in `servers.sh` and in the collector header.
- Exclusions in the responsive/a11y assertions (inline links exempt from the 24 px target rule; `aria-hidden` honeypot exempt) are WCAG-defensible and documented in-line rather than silently dropped.

**What is overstated or unverified:**

| # | Issue | Severity | Where |
| --- | --- | --- | --- |
| T1 | Visitor-facing and planning claims of automatic broker **retry** that does not exist (single attempt, one call site, no queue/job, `background-job-reliability` deliberately unrouted) | **Medium** | `app/enquire/received/page.tsx:61,79`; `app/api/visit-requests/route.ts:196`; `planning/05-lead-mutation-contract.md §8` |
| T2 | `seo-audit.json` `"problems": []` is cited as proof of clean crawl intent, but the collector cannot see the duplicate `robots` meta (first-match regex) and skips all metadata assertions on 404 routes, so the homepage canonical on error documents is untested | **Medium** | `scripts/collect-seo.mjs` `pick()` / `if (route.expect === "404") … continue` |
| T3 | `planning/06-capability-routing.md` cites three evidence artefacts that do not exist at the stated paths: `evidence/analytics/conversion-funnel-review.md`, `evidence/analytics/analytics-implementation-audit.md` (both merged into `analytics-and-funnel-review.md`), and `evidence/seo/content-discoverability-review.md` (**no such artefact in any form** — discoverability facts live only inside `seo-audit.json`) | **Medium** | routing table rows for `conversion-funnel-review`, `analytics-implementation-audit`, `content-discoverability-review` |
| T4 | All committed PNG evidence was **palette-quantised after capture** (128-colour `PLTE`, ~⅓ the byte size of a fresh Playwright capture) by a step that appears in no script and no documentation; `collect-all.sh` does not do it | **Low** | `evidence/visual-regression/*.png`, `evidence/browser/*.png` |
| T5 | `evidence/browser/filter-empty-state.json` contains only the hand-set literal `{"verified": true}` — the surrounding Playwright assertions are real, but the artefact itself proves nothing on its own | **Note** | `tests/browser-flows.spec.ts:401` |
| T6 | "Budgets, declared before measurement" cannot be corroborated from a single squashed commit and no planning document names the numbers | **Note** | `scripts/collect-performance.mjs:15` |
| T7 | The raised rate capacity on `:3100` is disclosed only in shell/script comments, not in any evidence JSON a scorer would read | **Low** | `scripts/servers.sh`, `collect-api-contract.mjs` header |
| T8 | No submission YAML and no scorer output exist in the run directory yet; all scoring language currently lives in prose. Nothing has been mis-scored — but nothing has been scored | **Note** | `runs/claude-code/` |

On T4 I checked rather than assumed: I compared a committed capture against my fresh re-run of the same test at the same viewport — identical dimensions (1280×6221), RMSE 0.157%. The images depict the same rendering; only colour depth was reduced. This is not fabricated evidence. It is, however, an undisclosed lossy transformation applied to artefacts whose stated purpose is byte-comparable regression evidence, and the responsive spec's own comment claims captures are "byte-stable".

I found **no** evidence file that was hand-written where a run was claimed, **no** test that passes vacuously, and **no** sign that any assertion was weakened to make a failing behaviour pass. The two prose artefacts (`deployment-constraint.md`, `analytics-and-funnel-review.md`) are self-evidently authored review records, not simulated tool output, and both cite machine-generated artefacts that I verified reproduce.

### Recommended scoring for disputed checks

| Check | Implementation's position | My recommendation |
| --- | --- | --- |
| `marketing-production-domain` | partial | **partial** — concur; keep the blocker |
| `marketing-seo-indexing` | (implied pass via `problems: []`) | **partial** — 404 crawl-signal conflict + collector blind spot |
| `marketing-provider-failure` | (implied pass) | **partial** — behaviour correct, recovery claim false |
| `marketing-performance` | pass with retained breach | **pass** — the retained failure is evidence of honesty |
| `marketing-structured-data` | pass | **pass** |
| `marketing-analytics` | pass | **pass** |
| `marketing-form-security` / `marketing-private-data` | pass | **pass** |
| `marketing-duplicate-submit` / `marketing-degraded-assets` | pass | **pass** |
| `marketing-browser-*` (3) | pass | **pass** |
| `marketing-routing-public-web` | routed | **partial** — `content-discoverability-review` has no artefact (T3) |

---

## Findings

**F1 — Medium — False automatic-retry claim shown to the visitor and asserted in planning.**
*Fact:* `notifyBroker` is invoked exactly once, from one call site; no retry loop, queue, scheduler or replay path exists.
*Impact:* a lead whose broker hand-off fails is told recovery is under way when nothing will happen until a human reads the database; `planning §8` misdescribes the system to future maintainers.
*Fix (either):* (a) implement a bounded retry (in-process backoff or a swept `notification_status='failed'` queue) and prove it with an evidence case that shows `notification_attempts > 1`; or (b) change the copy to what is true — "the hand-off has not confirmed; your request is recorded and the sales office has been alerted, please telephone and quote your reference" — and correct `planning §8`.
*Verification:* re-run `collect-api-contract.mjs` `broker-failure` asserting the corrected state, plus the `10-broker-failure` browser case.

**F2 — Medium — Conflicting robots directives and homepage canonical on 404 documents.**
*Fact:* live `/no-such-page` and `/residences/no-such-house` serve both `noindex` and `index, follow`, plus `<link rel="canonical" href="https://asteria-residences.example">`.
*Impact:* contradictory crawl signals; a soft-404 canonical pointing error documents at the homepage.
*Fix:* remove the blanket `robots: { index: true, follow: true }` and root `alternates.canonical` from `app/layout.tsx` (set them per-route), and emit no canonical on error documents.
*Verification:* extend `collect-seo.mjs` to collect **all** `robots` metas per document and to assert canonical/robots on 404 routes instead of `continue`-ing; re-run and require `problems: []` to mean something on those routes.

**F3 — Medium — Routing record cites three non-existent evidence paths.**
*Fix:* correct the two merged analytics rows to `evidence/analytics/analytics-and-funnel-review.md`, and either produce `evidence/seo/content-discoverability-review.md` or restate the row as "covered inside `seo-audit.json` (internal-link graph, sitemap parity, draft exclusion)".
*Verification:* a path-existence check over the routing table.

**F4 — Medium — Residence detail pages are served `Cache-Control: s-maxage=31536000` with no revalidation signal.**
*Fact:* `/` and `/residences/ridge-house-04` return a one-year shared-cache directive; `/residences` and `/enquire` are correctly `no-store`.
*Impact:* behind any CDN, a residence page — including its visible availability state *and* its `Offer` JSON-LD — could serve a year stale. The build's central structured-data virtue (no Offer on sold/reserved houses) would silently decay into the deceptive structured data this gate treats as blocking.
*Fix:* set an explicit `revalidate` (or tag-based revalidation on content change) for residence routes before any real deployment.
*Verification:* re-inspect live `Cache-Control` and confirm a content change propagates.

**F5 — Low — PNG evidence post-processed outside the recorded pipeline.**
*Fix:* either drop the quantisation and commit raw Playwright output, or add the step to `collect-all.sh` and state it in the responsive spec's comment (which currently claims byte-stable captures).

**F6 — Low — CSP permits `script-src 'unsafe-inline'`; no HSTS.**
*Impact:* the inline-script allowance materially weakens the XSS containment the CSP is there to provide; HSTS is untestable without TLS but must exist at deploy.
*Fix:* nonce or hash the framework bootstrap; add `Strict-Transport-Security` in the production deployment configuration and record it as a deploy-time obligation.

**F7 — Low — Sitemap `lastmod` for static and residence routes is build time, not content-change time.** Journal and legal entries correctly use real dates. *Fix:* derive from content metadata.

**F8 — Note — `robots.txt` uses a `Host:` directive** (Yandex-only; ignored by Google/Bing) and a trailing-slash origin. Harmless; remove or keep deliberately.

**F9 — Note — `evidence/browser/filter-empty-state.json` records a bare `{"verified": true}`.** *Fix:* record the observed counts ("Showing 3 of 12", the empty-state heading text, the post-reset count) so the artefact carries the finding rather than the claim.

---

## Required actions before this run could be Approved

1. Resolve **F1** (retry claim) — code or copy, plus corrected planning text and a re-run evidence case. Owner: implementer.
2. Resolve **F2** (404 crawl signals) **and** close the collector blind spot, then re-run `collect-seo.mjs`. Until then `marketing-seo-indexing` stays `partial`. Owner: implementer.
3. Correct **F3** (evidence-path citations). Owner: implementer.
4. Address **F4** (cache directive) or record an explicit accepted risk owned by a named party. Owner: implementer.
5. Disclose or remove the image post-processing (**F5**). Owner: implementer.
6. `marketing-production-domain` cannot be closed in this environment. It must remain `partial`, and the run must remain non-claimable. **A score must not be raised because remediation was described** — the corrected run and its evidence must exist.
7. Produce the submission YAML and deterministic scorer output; this review must be attached to it, alongside the independent Frontend Craft review.

## Residual risks

- All performance figures are loopback-emulated; real-network, CDN and TLS behaviour remain entirely unmeasured (disclosed by the run).
- Structured data was validated by parsing and truth-comparison only; no external Rich Results / schema validator was reachable.
- SQLite single-node persistence is appropriate here and disclosed as a scaling boundary, but no backup, retention or erasure-request mechanism exists for the lead table despite the privacy notice's commitments — out of this fixture's scope, worth carrying forward.

## Outcome

**Changes required**

Rationale: the build is substantially strong and, on the evidence I re-executed myself, genuinely production-*shaped* — the authoritative lead path, duplicate protection, secret boundary, analytics integrity, structured-data truthfulness and supply chain all hold up under independent attack, and the run's self-reporting of its own blocking failure is exemplary. But two declared blocking checks are not `pass` (`marketing-production-domain`, environmentally unavoidable; `marketing-seo-indexing`, fixable), a visitor-facing statement about recovery behaviour is untrue (F1), and the SEO evidence green-lights a property it does not test (F2). Under the reference-build gate, findings affecting a declared blocking check and benchmark truthfulness prevent approval. The run is **blocked and non-claimable** under `require_no_blockers` regardless of aggregate score.
