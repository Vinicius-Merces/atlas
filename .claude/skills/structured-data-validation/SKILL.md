---
name: structured-data-validation
description: "Validate JSON-LD and other structured data when public pages add or change schema markup, verifying syntax, page-content truthfulness, search eligibility, and non-conflicting canonical entities."
---

# Structured Data Validation

## Purpose

Verify that structured data accurately describes visible page content, uses appropriate schema types/properties, remains technically valid, and does not manufacture search signals or promise rich-result eligibility that the page cannot support.

## Trigger conditions

Use when a public page adds or changes JSON-LD, Microdata, RDFa, schema.org entities, Google-supported rich-result markup, organization/site identity markup, product/service/article/property/event markup, breadcrumbs, or related semantic metadata.

## Inputs

- Rendered page content and canonical URL
- Structured-data source/output
- Intended schema types and search features
- Product/content facts and authoritative source fields
- Current search-engine guidelines for the implemented feature
- Validation-tool output when available

## Procedure

1. Inventory every structured-data block on the rendered page, including framework-generated and third-party markup.
2. Identify the real entity or page meaning each block represents. Remove schema added merely because a template or library emitted it.
3. Prefer JSON-LD when it fits the existing stack, while accepting other valid formats when intentionally used.
4. Verify `@context`, `@type`, identifiers, URLs, dates, prices, availability, authorship, addresses, images, ratings/reviews, and nested entities against authoritative page/product data.
5. Structured data must describe content that users can reasonably find on the page when the applicable search feature requires that relationship. Never invent reviews, ratings, inventory, offers, authors, locations, dates, or business claims for markup.
6. Use stable canonical URLs and `@id` values for recurring entities where the architecture benefits from entity identity; avoid contradictory duplicate Organization/WebSite/Product/etc. nodes from multiple libraries.
7. Check required and recommended properties for the specific search feature against current official guidance rather than a remembered schema checklist.
8. Validate syntax and schema.org structure with an appropriate validator; when targeting Google rich results, also use the Rich Results Test or equivalent current Google validation surface.
9. Review errors, warnings, unsupported types, deprecated properties, malformed dates/URLs, wrong data types, and fields whose values disagree with visible content.
10. Ensure markup does not expose secrets, private identifiers, internal-only pricing, unpublished inventory, personal data, or other fields that should not be public.
11. Verify structured data survives the actual rendering path and is present on the canonical production-equivalent URL.
12. Revalidate after CMS/template changes that can silently duplicate or desynchronize markup across many pages.

## Outputs

- Structured-data inventory
- Entity/source-of-truth map
- Validator results
- Truthfulness/consistency findings
- Eligibility-specific findings
- Duplicate/conflicting-entity findings
- Required corrections and residual limitations

## Limitations

- Valid markup does not guarantee a rich result, indexing, ranking, or search presentation.
- Schema.org validity and search-engine feature eligibility are related but not identical checks.
- Do not add unsupported or misleading markup solely to chase a richer search appearance.

## Dependencies

- Rendered public-page output and canonical URL
- Authoritative content/product data
- Current schema.org and target search-engine feature guidance
- `seo-technical-audit` for crawl/index/canonical prerequisites

## Validation

- Parse every rendered structured-data block successfully.
- Run generic schema validation and the target search feature validator where applicable.
- Compare high-value properties against visible/authoritative data rather than only validator acceptance.
- Verify no duplicate block contradicts the canonical entity/page facts.
- Record that rich-result display remains search-engine controlled even when validation passes.
