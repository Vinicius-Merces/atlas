---
name: content-discoverability-review
description: "Review content discoverability when information architecture, internal links, semantic structure, rendering, topic/entity organization, or AI/search visibility changes, aligning human navigation with crawlable authoritative content."
---

# Content Discoverability Review

## Purpose

Review whether important content can be found, understood, navigated, crawled, and connected by people and search/AI discovery systems without inventing special optimization hacks or weakening content quality.

## Trigger conditions

Use when changing site information architecture, navigation, internal linking, content hubs, article/product/service structure, headings/semantic HTML, JavaScript-rendered content, pagination, archives, topic/entity organization, or search/AI discoverability strategy.

## Inputs

- Content inventory and target audiences/tasks
- Site/navigation/information architecture
- Important landing/content pages and canonical URLs
- Internal-link graph or representative crawl evidence
- Rendering approach
- Content ownership/freshness model
- Existing technical SEO and structured-data evidence
- Current official search-platform guidance when making AI-search-specific recommendations
- Search Console/analytics evidence when available

## Procedure

1. Identify the content that must be discoverable, the user intent/task it serves, and the authoritative owner/source for each content type.
2. Map hierarchy from home/navigation/hubs to detail pages and identify orphaned, buried, duplicated, or competing content.
3. Review descriptive navigation labels, headings, semantic landmarks, anchor text, breadcrumbs, related-content links, and contextual links for human clarity first.
4. Ensure important content and links are present in crawlable rendered output and are not dependent on interactions that discovery systems or accessibility tools cannot reliably traverse.
5. Review canonical URL ownership, duplication, pagination/archive/facet behavior, and content consolidation with `seo-technical-audit` where technical indexing rules are involved.
6. Review topic/entity naming consistency across titles, headings, URLs, content, metadata, and structured data without forcing repetitive keywords.
7. Use `structured-data-validation` when entity markup exists; structured data must describe real visible/authoritative content rather than substitute for it.
8. Assess images/video/other media for useful surrounding text, labels, captions, and landing-page context when they carry material information.
9. Review freshness, dates/version signals, stale content, superseded pages, and internal links pointing to deprecated material.
10. For AI-oriented discovery, preserve the same crawlability, people-first usefulness, technical SEO, accessible-content, and authoritative-source principles. Do not invent unsupported LLM-only markup or promise inclusion.
11. For Google Search AI features, current official guidance should be treated as authoritative for Google-specific claims: normal SEO/indexability remains foundational and no special AI-only markup or machine-readable text file is required for inclusion. Re-check official guidance before publishing a recommendation because this area changes quickly.
12. Do not present `llms.txt`, AI-specific text files, or a special schema as a Google Search requirement. Evaluate such files separately only when another explicit consumer/runtime has a documented use for them.
13. Prefer unique, useful, non-commodity content, clear firsthand expertise/evidence, and well-supported media over scaled pages created only to target speculative AI/GEO/AEO queries.
14. When Search Console exposes generative-AI-specific performance reporting for the property, use it as measurement evidence. Do not assume the report is universally available, and do not infer causality from impression/click changes alone.
15. Consider agent/browser interaction readiness only when it serves a real product use case. Semantic HTML, accessible controls, stable URLs, explicit forms/actions, and clear authorization boundaries are more durable than speculative agent-only markup.
16. Identify content gaps only when a real user/business information need is unsupported, not merely because a keyword/tool suggests producing more pages.
17. Record discoverability evidence separately from ranking, traffic, AI citation, and conversion expectations.

## Outputs

- Content hierarchy/discovery map
- Orphan/depth/internal-link findings
- Semantic/rendering findings
- Entity/topic consistency findings
- Freshness/duplication findings
- AI-search guidance source/freshness note when material
- Search Console/analytics evidence and availability limits when used
- Prioritized content architecture recommendations and limitations

## Dependencies

- `seo-technical-audit` for crawl/index/canonical mechanics
- `structured-data-validation` where schema markup exists
- `content-quality-review` for clarity and audience fit
- `browser-flow-validation` when navigation/rendering must be observed directly

## Limitations

- Discoverability does not guarantee ranking, traffic, AI citation, Discover inclusion, or conversion.
- No special AI-search markup replaces normal crawlability and useful authoritative content.
- Platform-specific AI-search features and reporting are temporally unstable; current official guidance must be rechecked for externally visible claims.
- Search Console visibility reports, when available, measure observed performance and do not prove why a page was or was not selected by an AI/search system.

## Validation

- Crawl or manually trace representative important pages from navigation/hubs and identify orphaned or excessive-depth paths.
- Inspect rendered DOM/links for JavaScript-driven navigation and content.
- Verify canonical/structured-data signals through the dedicated skills when applicable.
- Verify AI-search-specific recommendations against current official documentation before treating them as requirements.
- Confirm recommendations improve real human information access as well as machine discovery rather than producing keyword-only or speculative AI-only pages.
