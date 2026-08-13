---
name: application-search-design
description: "Design product/content search with source-of-truth fields, query semantics, ranking, filters, pagination, indexing, authorization, tenant scope, freshness, failure states, and database-versus-search-engine tradeoffs."
---

# Application Search Design

## Purpose

Design search around user intent, authoritative data, access control, relevance, and freshness before selecting a search technology.

## Trigger conditions

Use for keyword search, command palettes, property/product/content discovery, faceted filters, autocomplete, full-text search, search APIs, or migration to a dedicated search engine.

## Inputs

- Search journeys and representative queries
- Authoritative entities/fields and access rules
- Dataset size, update frequency, and latency targets
- Ranking/filter/sort requirements
- Current database/index/search infrastructure

## Procedure

1. Define searchable documents/entities, user intent, result unit, and authoritative source.
2. Separate exact lookup, structured filters, substring/prefix, full-text, semantic/vector, and recommendation needs.
3. Design normalization, tokenization/language behavior, typo tolerance, ranking signals, tie-breaking, and deterministic sort fallbacks as applicable.
4. Keep authorization and tenant scope inside the query boundary; never fetch broad results then rely only on client filtering.
5. Choose cursor/offset pagination according to ordering stability and result scale.
6. Match database indexes/full-text capabilities to evidence before introducing a separate search service.
7. If using an external index, define change propagation, freshness SLA, deletion, backfill, reindex, alias/version transition, and reconciliation.
8. Design zero-results, loading, malformed query, unavailable index, partial/degraded result, and mobile filter UX.
9. Measure relevance with representative queries rather than anecdotal happy paths.

## Outputs

- Search intent and document model
- Query/filter/ranking contract
- Index/technology decision
- Authorization/freshness/reindex design
- Relevance and failure-path evidence

## Dependencies

- `database-schema-review` for database-backed indexes and query fit
- `authorization-boundary-review` / `saas-multitenancy-review` for protected search
- `external-api-resilience-review` when a remote search provider is used
- `responsive-layout-audit` for complex search/filter UI

## Limitations

No ranking approach guarantees relevance without domain queries and evaluation. Vector search is not automatically better than lexical or structured search.

## Validation

- Run representative known-item, exploratory, typo/edge, zero-result, protected, cross-tenant, pagination, and stale-index cases.
- Inspect query plans or provider diagnostics for material paths.
- Verify deletion/permission changes disappear from results within the declared freshness boundary.
