---
name: seo-technical-audit
description: "Audit technical SEO when public web routes, domains, redirects, metadata, robots, sitemaps, canonicals, rendering, status codes, or crawl/index behavior change."
---

# SEO Technical Audit

## Purpose

Verify that public web content intended for organic discovery is technically reachable, crawlable, renderable, canonically consistent, and indexable by design without claiming rankings that cannot be guaranteed.

## Trigger conditions

Use when a public website, domain, route structure, CMS, rendering mode, redirect, robots rule, sitemap, canonical URL, metadata strategy, localization, or indexing behavior changes.

## Inputs

- Production or production-equivalent public URLs
- Route and redirect inventory
- HTML/head output and HTTP response headers
- `robots.txt`, robots meta/X-Robots-Tag rules, and sitemap files
- Canonical-domain/URL policy
- Rendering architecture and internal-link structure
- Search Console or crawler evidence when available

## Procedure

1. Classify public URLs as intended-indexable, intentionally non-indexable, redirect, error, duplicate/alternate, or private.
2. Verify indexable pages return appropriate successful HTTP status and meaningful rendered content without requiring an authenticated session.
3. Inspect redirect chains, protocol/host variants, trailing-slash/query behavior, legacy routes, and canonical-domain redirects. Avoid loops and unnecessary chains.
4. Validate canonical signals. `rel="canonical"`, redirects, and sitemap inclusion must not contradict one another or point indexable pages toward errors, non-indexable pages, or unrelated content.
5. Inspect `robots.txt` as crawl-control, not as a substitute for access control or reliable deindexing. Ensure important HTML, CSS, JavaScript, images, or rendering resources are not accidentally blocked.
6. Inspect robots meta and X-Robots-Tag directives. Remember that a crawler must be able to fetch a page to observe a `noindex` directive.
7. Validate sitemap files: reachable, parseable, scoped to the intended site, containing canonical indexable URLs rather than redirects/errors/noindex URLs, and reflecting current routes.
8. Verify titles, meta descriptions where used, canonical links, language/locale metadata, and social metadata are route-specific where the product requires them and do not contain placeholder or stale domain values.
9. Verify semantic crawlable internal links to important pages. Do not rely solely on click handlers or client state for discoverability.
10. Test direct fetch/render behavior for JavaScript applications, including initial HTML, hydration, status codes, and whether essential content/links are available to the intended crawler path.
11. Review duplicate/faceted/query URL behavior and define canonicalization/index policy instead of allowing accidental URL multiplication.
12. Review pagination, localized routes/hreflang, image/video/news sitemap extensions, or other specialized search surfaces only when actually present.
13. Compare declared sitemap/canonical/robots behavior against deployed behavior. Configuration files alone are not sufficient evidence.
14. Record findings separately as crawlability, indexability, canonicalization, rendering, metadata, internal-discovery, or operational/Search Console issues.

## Outputs

- URL intent/indexability matrix
- Redirect/canonical findings
- Robots/noindex findings
- Sitemap findings
- Rendered metadata/content findings
- Internal-discovery findings
- Blocking SEO defects and residual risks

## Limitations

- Passing this audit does not guarantee ranking, indexing, rich results, traffic, or a specific search-engine outcome.
- SEO product/content strategy is broader than technical crawl/index health.
- `robots.txt` is not an authentication or confidentiality mechanism.

## Dependencies

- Deployed or production-equivalent HTTP behavior
- Canonical domain and route intent
- Browser/fetch/crawler evidence where available
- `structured-data-validation` when schema markup is present
- `browser-flow-validation` when client rendering/navigation can affect public-page behavior

## Validation

- Fetch representative indexable, noindex, redirect, duplicate, and error URLs and record status/headers/body evidence.
- Verify `robots.txt`, sitemap, canonical, and robots directives do not conflict for representative URLs.
- Validate direct navigation/rendering for important public pages.
- Confirm generated sitemap URLs resolve as intended and do not systematically point to redirects, errors, or non-indexable pages.
- Treat unknown production behavior as missing evidence rather than assuming framework configuration is deployed correctly.
