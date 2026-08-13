---
name: cms-content-modeling
description: "Design content models and editorial workflows for websites and content-driven products, covering content types, structured fields, slugs, drafts, preview, localization, media, authorship, publishing lifecycle, references, SEO data, migrations, and frontend rendering contracts."
---

# CMS Content Modeling

## Purpose

Model content as reusable structured product data so editors can publish safely without forcing the frontend into page-builder entropy or hard-coded copy.

## Trigger conditions

Use for blogs, landing-page collections, documentation, real-estate listings, products, projects/portfolio, localized pages, editorial sites, or CMS migrations.

## Inputs

- Content inventory and editorial roles
- Page/entity types and reusable content blocks
- Publishing/draft/preview requirements
- Localization and media requirements
- SEO/structured-data/discoverability needs

## Procedure

1. Identify durable content entities and relationships before defining visual page blocks.
2. Separate semantic fields from presentation-only controls; allow design direction without exposing arbitrary styling knobs by default.
3. Define stable identifiers, slugs, canonical URLs, redirects, references, ownership, authorship, and taxonomy.
4. Model draft, scheduled, published, archived, and deleted states plus preview authorization.
5. Define localization strategy per field/entity and fallback behavior explicitly.
6. Model media references through the upload/storage lifecycle rather than embedding uncontrolled URLs.
7. Include SEO metadata only where editors can supply truthful values; derive defaults from authoritative content where practical.
8. Define schema evolution/content migration and how old entries remain renderable during rollout.
9. Design frontend rendering contracts, empty/optional fields, long content, rich text portability, and unknown block handling.
10. Validate editor workflows and rendered output, not only the content schema.

## Outputs

- Content entity/reference model
- Editorial state and permission model
- Localization/media/SEO strategy
- Frontend rendering contract
- Migration and preview plan

## Dependencies

- `content-discoverability-review` and `seo-technical-audit` for public content
- `structured-data-validation` when content feeds schema markup
- `file-upload-storage-design` for media
- `authorization-boundary-review` for editorial/admin access

## Limitations

This skill is CMS-vendor neutral. A visual page builder may be appropriate, but should be admitted intentionally because unrestricted layout controls can erode consistency and accessibility.

## Validation

- Create representative draft/published/localized entries with optional and long content.
- Verify preview access, canonical/slug changes, redirect behavior, unknown blocks, and rendering fallbacks.
- Rehearse a content-model migration on non-empty data when schema changes are material.
