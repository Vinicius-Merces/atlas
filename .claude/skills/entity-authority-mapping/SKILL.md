---
name: entity-authority-mapping
description: "Map public entities, factual claims, evidence owners, canonical sources, and conflicts before GEO, schema, knowledge-content, or AI-search work."
---

# Entity Authority Mapping

## Purpose
Create a traceable source-of-truth model for public entities and factual claims so GEO, SEO, structured data, content, and AI-search work can reuse consistent evidence instead of inventing or duplicating authority.

## Trigger conditions
Activate before creating or expanding entity pages, organization/person/product/location schema, answer-ready content, knowledge-base claims, AI-search recommendations, or public facts that appear in more than one surface.

## Inputs
Required:
- public pages and routes that describe the organization, products/services, people, locations, policies, proof, and published content;
- canonical business facts and accountable owners;
- metadata, structured data, feeds, CMS records, or other public representations that can conflict with rendered content.

Optional:
- sales collateral, directories, public profiles, press references, research, partner pages, locale variants, and freshness/update records.

## Procedure
1. Inventory entities that materially affect a user or buyer decision: organization, offer, product, person, location, policy, proof, and published content.
2. For each entity, record canonical name, identifier/URL, accountable owner, claim set, source evidence, update cadence, locale equivalents, and public/private status.
3. Separate first-party facts, third-party evidence, inferred relationships, and unsupported claims. Never collapse them into one undifferentiated “authority” score.
4. Detect conflicting facts across rendered pages, CMS records, metadata, schema, feeds, public profiles, documentation, and sales collateral.
5. Mark unsupported claims for removal, qualification, or evidence collection. Do not preserve a claim merely because it would be useful for SEO or GEO.
6. Define one canonical source for each material fact and identify the rendered page that explains the entity to a human.
7. Record freshness expectations and the event or owner responsible for updating time-sensitive facts such as prices, locations, availability, policies, credentials, and team roles.
8. Feed confirmed entities and conflicts into GEO, SEO, schema, localization, content, and measurement work with explicit evidence references.

## Output
A traceable entity ledger containing: entity → canonical URL/identifier → factual claims → evidence source → accountable owner → freshness/update rule → locale equivalents → conflicts → remediation status.

## Dependencies
- Access to canonical business/product facts and the people accountable for them.
- `structured-data-validation` when entity facts are represented in schema.
- `seo-technical-audit` when canonicalization, redirects, indexation, or route duplication affect the entity source-of-truth.
- `generative-engine-optimization` when the mapping is part of a broader GEO initiative.

## Limitations
- This skill cannot manufacture external authority, expertise, reviews, certifications, customers, awards, availability, or third-party references.
- Private operational data is not public GEO material by default and must not be exposed merely to strengthen an entity profile.
- A public mention is not automatically authoritative; provenance, context, freshness, and ownership still matter.
- Conflicting business facts require escalation to an accountable owner when the canonical value cannot be established from evidence.

## Validation
- Every material entity has a canonical identifier or URL, accountable owner, and at least one inspectable source.
- Material claims are classified as supported, unsupported, inferred, or conflicting.
- Conflicts across page content, metadata, schema, feeds, profiles, and locale variants are either resolved or explicitly blocked/escalated.
- Time-sensitive facts have freshness expectations or update ownership.
- No private or fabricated evidence is introduced to make an entity appear more authoritative.
