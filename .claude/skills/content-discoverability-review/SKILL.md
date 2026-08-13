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
10. For AI-oriented discovery, follow the same crawlability, people-first usefulness, technical SEO, and accessible-content principles; do not invent unsupported LLM-only markup or promise inclusion.
11. Identify content gaps only when a real user/business information need is unsupported, not merely because a keyword/tool suggests producing more pages.
12. Record discoverability evidence separately from ranking/traffic expectations.

## Outputs

- Content hierarchy/discovery map
- Orphan/depth/internal-link findings
- Semantic/rendering findings
- Entity/topic consistency findings
- Freshness/duplication findings
- Prioritized content architecture recommendations and limitations

## Dependencies

- `seo-technical-audit` for crawl/index/canonical mechanics
- `structured-data-validation` where schema markup exists
- `content-quality-review` for clarity and audience fit
- `browser-flow-validation` when navigation/rendering must be observed directly

## Limitations

- Discoverability does not guarantee ranking, traffic, AI citation, Discover inclusion, or conversion.
- No special AI-search markup replaces normal crawlability and useful authoritative content.
- Search-engine behavior can change; current official guidance should be rechecked for externally visible claims.

## Validation

- Crawl or manually trace representative important pages from navigation/hubs and identify orphaned or excessive-depth paths.
- Inspect rendered DOM/links for JavaScript-driven navigation and content.
- Verify canonical/structured-data signals through the dedicated skills when applicable.
- Confirm recommendations improve real human information access as well as machine discovery rather than producing keyword-only pages.
