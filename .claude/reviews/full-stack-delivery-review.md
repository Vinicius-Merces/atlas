# Full-Stack Delivery Review

## Purpose

Independently determine whether a website or SaaS built under the Full-Stack Delivery model is genuinely production-ready rather than merely implemented.

## Independence

The reviewer should not be the sole implementer of the work being approved.

## Review areas

### Product and architecture
- Brief outcomes and acceptance criteria remain traceable to implementation.
- Architecture and authoritative state are explicit.
- Technology choices are justified by requirements rather than trend.

### Delivery primitives
- Applicable forms/mutations, files, search, imports/exports, email, notifications, rate controls, CMS, audit, admin operations and flags follow their canonical skills.
- Non-applicable primitives are omitted intentionally rather than left half-built.

### Trust and reliability
- Authentication, authorization, tenant boundaries, secrets, jobs, cache, providers, payments and webhooks preserve existing trust gates where applicable.
- Failure, retry, duplicate, stale, partial and recovery behavior has evidence.

### Premium frontend
- Significant user-facing work has a defensible visual thesis and does not regress into generic component-library/template defaults.
- Responsive, accessibility, visual regression, browser and performance evidence exists.
- Loading, empty, error, disabled, offline/degraded and success states are product-quality UI, not afterthoughts.

### Public web and discoverability
- Public sites preserve content, technical SEO, structured-data, analytics/conversion and supply-chain gates where applicable.

### Operations
- Privileged/admin actions are bounded and auditable.
- Observability and reconciliation exist where distributed state can diverge.
- Flags, files, exports and other temporary/lifecycle resources have cleanup ownership.

## Blocking findings

Critical or High findings involving trust-boundary escape, cross-tenant exposure, irreversible duplicate effects, privileged action ambiguity, broken primary journeys, inaccessible required interaction, severe responsive breakage, or fabricated financial/search/structured-data claims block approval.

## Outcome

Return one of: **Approved**, **Approved with conditions**, **Changes required**, or **Blocked**. Include evidence, owners and verification steps for every unresolved condition.
