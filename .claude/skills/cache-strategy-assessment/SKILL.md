---
name: cache-strategy-assessment
description: "Assess caching when browser, CDN, edge, server, database, runtime, or distributed caches change, verifying key scope, freshness, invalidation, authorization safety, stampede control, and consistency tradeoffs."
---

# Cache Strategy Assessment

## Purpose

Decide what should be cached, where, for how long, under which identity/variant key, and how stale or invalid state is detected and corrected without leaking protected data.

## Trigger conditions

Use when adding or changing browser/CDN/edge/server/runtime/distributed caches, response caching, memoization, cached database queries, cache tags, revalidation, TTLs, stale-while-revalidate, negative caching, or cache-backed rate/feature state.

## Inputs

- Data/request classification and sensitivity
- Authoritative source and mutation paths
- Cache layers and provider/framework semantics
- Key construction and variants
- TTL/freshness/revalidation/invalidation rules
- Traffic, latency, consistency, and failure requirements

## Procedure

1. State the cache objective: latency, origin protection, cost reduction, offline resilience, expensive-computation reuse, or another measurable goal.
2. Identify the authoritative source and determine whether cached state may be public, shared, private/user-specific, tenant-specific, or never cached.
3. Review cache keys for tenant, user/authorization scope, locale, currency, feature variant, query parameters, content negotiation, version, and other state that changes the representation.
4. Verify shared caches cannot serve one user's or tenant's protected response to another principal.
5. Define freshness explicitly using TTL/validators/tags/events or another mechanism. Distinguish freshness from correctness and availability.
6. Map every mutation path to invalidation/revalidation behavior; avoid relying on undocumented eventual expiry for correctness-critical state.
7. Decide when stale serving is acceptable, for how long, and under which failure conditions; never serve stale security/permission state merely for availability.
8. Review stampede/thundering-herd protection using request coalescing, locking, jittered TTLs, prewarming, stale serving, or admission controls where justified.
9. Review negative caching and error caching so transient failures do not become durable false state.
10. Assess eviction/capacity behavior, hot keys, oversized values, serialization cost, connection limits, and cache-unavailable degradation.
11. Review write-through/write-behind/read-through or framework-specific behavior for race conditions and source-of-truth ambiguity.
12. Instrument hit/miss ratio, origin load, age/staleness, revalidation failures, evictions, key cardinality, and latency only when those metrics inform decisions.

## Outputs

- Cache admission/layer map
- Key and authorization-scope findings
- Freshness/invalidation model
- Stampede/capacity findings
- Degradation/consistency findings
- Required changes, tests, and residual risk

## Dependencies

- Current cache/provider/framework semantics
- `authorization-boundary-review` for protected cached resources
- `saas-multitenancy-review` for tenant-sensitive caches
- `web-performance-field-readiness` for public web caching/performance interactions

## Limitations

- Caching is optional; complexity without measured benefit is a valid reason not to cache.
- Framework cache defaults can change and must be verified for the deployed version.
- Hit ratio alone does not prove correctness or user benefit.

## Validation

- Exercise hit, miss, stale, invalidation/revalidation, cache-unavailable, and mutation-after-cache paths.
- Verify user/tenant/locale/variant boundaries cannot collide in keys for protected or differentiated content.
- Confirm authorization or role changes are not masked by unsafe stale/shared cache state.
- Measure origin/load/latency impact when the cache exists primarily for performance or cost.
