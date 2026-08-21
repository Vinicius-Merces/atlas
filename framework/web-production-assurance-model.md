# Web Production Assurance Model

## Purpose

ATLAS uses this model to prove that a public web release is not merely implemented, but demonstrably usable in a real browser, technically discoverable when discovery is intended, semantically truthful to search systems, protected by proportionate browser/edge controls when material, and free from unreviewed high-risk supply-chain changes.

This model complements rather than replaces:

- `framework/frontend-craft-model.md` for authored visual/responsive quality;
- `framework/saas-production-trust-model.md` for identity, authorization, data, secrets, payments, and provider trust;
- `framework/web-security-edge-assurance-model.md` for CSP/security headers, sensitive public-path exposure, CDN/WAF/bot behavior, and crawler-aware edge assurance;
- general QA, accessibility, performance, security, privacy, and release gates.

## Core principle

**Rendered behavior, deployed HTTP evidence, effective security/discovery behavior, truthful metadata, and dependency provenance before release claims.**

A build can compile while critical navigation fails. A page can render while canonical/robots behavior prevents intended discovery. A correct `robots.txt` can coexist with a WAF rule that blocks the intended crawler. A CSP can improve security while silently breaking analytics, conversion, auth, payments, chat, or APIs. JSON-LD can validate syntactically while describing invented facts. A dependency can fix a feature while silently expanding execution risk. Production assurance must inspect those boundaries directly.

## Assurance path

```text
route and release intent
        ↓
supply-chain delta when dependencies/build inputs changed
        ↓
critical browser journeys
        ↓
browser/edge security when material
        ↓
HTTP + crawl/index behavior for public pages
        ↓
structured-data truth and validation when present
        ↓
independent web-production assurance review
        ↓
evidence + continuity
```

Not every gate applies to every change. Non-applicability must be explained by architecture or scope, not assumed.

## 1. Browser-flow evidence

Use `browser-flow-validation` for release-critical journeys.

Browser evidence should answer:

- Can a user reach the route directly and through intended navigation?
- Do forms, async states, redirects, and critical integrations reach observable outcomes?
- Are uncaught runtime exceptions, console failures, or failed requests hiding behind a visually plausible page?
- Does authentication/session state behave correctly when part of the journey?
- Do representative mobile and desktop interaction paths still work?
- Can a failed journey be reproduced from saved evidence?

Use project-native E2E tooling where possible. Playwright is a strong default for new browser automation because its browser assertions auto-wait and its isolation model supports independent browser contexts, but ATLAS does not require replacing a healthy existing E2E stack merely for uniformity.

Browser-flow validation is behavioral. `visual-regression-review` remains responsible for pixel/composition regressions, and `responsive-layout-audit` remains responsible for deeper layout authorship across viewport classes.

## 2. Browser and edge security evidence

Use `web-security-header-audit` when CSP/security headers, third-party runtime origins, or public sensitive-path exposure are material. Use `crawler-edge-access-audit` when CDN/WAF/bot/challenge controls can affect intended SEO/GEO discovery.

The security-edge boundary separates:

- **header intent:** what the framework/server intends to emit;
- **effective response:** what the browser/crawler actually receives after proxies/CDNs;
- **CSP execution policy:** which origins and browser capabilities are allowed;
- **integration compatibility:** whether trusted analytics, conversion, chat, auth, payment, API, storage, font/image, and monitoring traffic still works;
- **sensitive-path exposure:** whether common private configuration paths return usable secrets;
- **edge enforcement:** which WAF/bot/challenge/geo/IP/rate-limit/access rule can terminate a request before application code;
- **crawler identity evidence:** whether the result is only user-agent simulation or verified provider/security-event evidence.

A security header that exists in source is not production evidence. A `200` status is not crawler success when the body is a challenge/interstitial or degraded shell. A simulated Google/OpenAI/Claude/Perplexity user agent is diagnostic, not proof that the proprietary crawler is verified or allowed.

Security hardening must not be achieved by disabling release-critical integrations or by adding broad wildcard/bot/datacenter allowlists merely to make automation green.

## 3. Technical SEO evidence

Use `seo-technical-audit` when public discovery matters.

The audit separates:

- **crawlability:** can the crawler fetch the resource and the resources required to understand it?
- **indexability:** is indexing intentionally allowed or denied?
- **canonicalization:** do redirects, canonical annotations, and sitemap signals agree on the preferred URL?
- **rendering:** does the deployed response expose meaningful content/links through the intended rendering path?
- **URL health:** do indexable URLs return appropriate successful status rather than redirects/errors/soft failures?
- **internal discovery:** can important pages be reached through crawlable links?
- **metadata:** do titles, descriptions, canonical links, locale signals, and public-domain values match the current route/product?

`robots.txt` is primarily crawl control. It must not be treated as confidentiality or as a reliable replacement for `noindex`. Conversely, a `noindex` directive must remain fetchable by the intended crawler so the directive can be observed.

When edge security can alter crawler responses, technical SEO evidence must be reconciled with `crawler-edge-access-audit`; `robots.txt` alone cannot prove accessibility.

Sitemaps should represent canonical URLs the product actually intends search systems to discover, not a dump of every generated route.

Passing technical SEO does not guarantee ranking, indexing, traffic, or a particular search presentation.

## 4. Structured-data truth

Use `structured-data-validation` whenever schema markup is emitted.

Structured data is application data published to search systems. It must therefore have a source of truth.

Rules:

1. Markup describes the real page/entity, not the keyword strategy the team wishes were true.
2. Ratings, reviews, authors, offers, availability, locations, dates, prices, and other factual fields cannot be fabricated to satisfy a schema type.
3. Required/recommended properties come from current feature guidance, not stale memory.
4. Generic schema validity and search-feature eligibility are separate checks.
5. Duplicate libraries/templates must not emit conflicting representations of the same canonical entity.
6. Validation passing is evidence of markup quality, not a guarantee of rich-result display.

Google currently recommends JSON-LD when it fits the implementation because it is generally easier to maintain, but valid Microdata/RDFa remain acceptable when intentionally used.

## 5. Supply-chain assurance

Use `supply-chain-risk-audit` for changes to dependencies or executable build inputs.

The review covers:

- manifest and lockfile delta;
- direct and transitive vulnerability/malware evidence;
- package/registry/source identity;
- lifecycle/install/build scripts;
- provenance and integrity behavior;
- maintainer/upstream change signals proportional to risk;
- CI actions/plugins and container/base-image inputs;
- runtime reach/blast radius;
- rollback/removal and ongoing advisory detection.

Dependency review should happen at change time, not only after vulnerable code is already merged. Repository-native dependency review/advisory features and ecosystem tooling should be used when available, but their absence or a clean report is not by itself proof of safety.

## 6. Evidence model

A release claim should name the evidence actually obtained:

- browser journeys, browser/runtime, viewport, environment, test state, and diagnostics;
- effective security headers/CSP and critical integration behavior when material;
- passive sensitive-path and edge/crawler evidence without secret values when material;
- representative HTTP responses, redirects, headers, canonical/robots/sitemap behavior;
- structured-data parser/validator output and truth-source comparison;
- dependency diff, advisory/dependency-review result, script/provenance inspection;
- unavailable evidence and residual risk.

Avoid phrases such as "SEO-ready", "production-ready", "fully tested", "secure", "crawler-safe", or "secure dependencies" when the corresponding evidence was not executed.

## 7. Independent review

Significant public-web releases use `.claude/reviews/web-production-assurance-review.md` after implementation and applicable validation. Significant security-header/edge work also uses `.claude/reviews/web-security-edge-assurance-review.md`.

The sole implementer may supply evidence and fix findings but must not be the only approver of their own significant work.

Unresolved Critical or High findings block approval. Missing mandatory evidence for a release-critical journey, security/edge boundary, intended indexable route, factual structured-data claim, or high-risk dependency delta prevents an unconditional Approved outcome.

## 8. Relationship to release sequencing

For a significant public SaaS/web change, a robust ATLAS path may be:

```text
frontend craft
    +
SaaS production trust when applicable
    +
web security/edge assurance when applicable
    +
web production assurance
    +
release/deployment integrity
```

These are orthogonal gates, not different names for the same review.

## External assurance basis

This model is original ATLAS guidance. Its behavior is cross-checked against current primary documentation such as browser/platform CSP guidance, CDN/WAF/bot provider documentation, Google Search Central for crawl/index/canonical/sitemap/structured-data behavior, Playwright documentation for browser assertions/isolation/evidence, and GitHub supply-chain/dependency-review guidance. Current provider/tool documentation remains authoritative when implementation details change.
