---
name: analytics-implementation-audit
description: "Audit product analytics implementation when events, properties, identity, consent, ecommerce, client/server collection, destinations, or decision metrics change, verifying taxonomy parity and trustworthy measurement."
---

# Analytics Implementation Audit

## Purpose

Verify that implemented analytics accurately represents the canonical event taxonomy and product decisions, without duplicate firing, missing context, unsafe personal data, identity confusion, or environment contamination.

## Trigger conditions

Use when adding/changing analytics events, ecommerce measurement, tags/SDKs, client/server event collection, Measurement Protocol or equivalent, identity stitching, consent behavior, destinations, funnels, experiments, or KPI instrumentation.

## Inputs

- Canonical event taxonomy and metric definitions
- Instrumentation code/tag configuration
- Client/server event paths
- Identity/session model
- Consent/privacy rules
- Analytics destination/debug tooling
- Representative browser/network/server evidence

## Procedure

1. Map each business decision/metric to the events and properties required to compute it; reject events with no decision or operational purpose unless intentionally diagnostic.
2. Compare implemented event names, property names, types, required/optional fields, units, currency, item arrays, and semantic timing with the canonical taxonomy.
3. Check duplicate firing across client navigation, hydration, retries, tag managers, server collection, workers, and webhook/provider paths.
4. Check missing events on refresh, direct navigation, error paths, retries, offline/server-side actions, or SPA route changes where applicable.
5. Review identity/session/user stitching for anonymous-to-authenticated transitions, cross-device expectations, tenant scope, resets/logouts, and stale identifiers.
6. Verify client and server events use stable event/transaction identifiers where deduplication is needed.
7. Audit personal/sensitive data, URLs/query strings, free text, user IDs, IP-related configuration, consent/opt-out, retention, and downstream sharing against project privacy policy.
8. Separate development/preview/test traffic and credentials from production measurement where practical.
9. Validate ecommerce/value events against authoritative business state; purchases/refunds must not rely solely on a browser success page.
10. Use provider debug/realtime/network tools to inspect actual payloads and destination receipt, not only source code.
11. Reconcile analytics totals against another authoritative source for high-value conversions when feasible, documenting expected differences.
12. Record sampling, attribution, identity, ad-blocking, consent, latency, and provider-processing limitations before turning data into product conclusions.

## Outputs

- Taxonomy-to-implementation matrix
- Missing/duplicate event findings
- Property/type/value findings
- Identity/deduplication findings
- Privacy/consent findings
- Destination/reconciliation evidence and residual measurement limits

## Dependencies

- Canonical analytics/event taxonomy
- Provider debug or destination inspection tools when available
- `event-taxonomy-design` when taxonomy itself is incomplete
- `privacy-impact-assessment` when collection meaningfully changes personal-data processing

## Limitations

- Destination reporting latency, attribution, sampling, consent, blockers, and provider processing can create expected differences.
- Receiving an HTTP success from a collection endpoint does not prove an event is queryable in final reports.
- Does not define business KPIs when product strategy is unresolved.

## Validation

- Trigger representative events and inspect actual client/server payloads plus provider debug/realtime receipt where available.
- Confirm no duplicate purchase/lead/signup event is produced by refresh, retry, hydration, or parallel collection paths.
- Verify consent/opt-out state changes collection behavior as designed.
- Reconcile at least one high-value conversion/event against authoritative application or transaction data when feasible.
