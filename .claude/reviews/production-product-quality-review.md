# Production Systems & Product Quality Review Gate

## Review type

Independent P1 production-systems and product/growth quality review.

## Scope

Evaluate material changes across database integrity, multitenancy, asynchronous jobs, caching, conversion funnels, analytics implementation, and content discoverability, including their composition with existing P0 trust/web/frontend gates.

## Evidence inspected

- Request, acceptance criteria, risk, and affected architecture
- Schema/migration/query evidence where applicable
- Tenant/resource isolation and quota evidence where applicable
- Queue/job retry/idempotency/dead-letter evidence where applicable
- Cache key/freshness/invalidation evidence where applicable
- Funnel/browser/downstream handoff evidence where applicable
- Analytics taxonomy/payload/destination/reconciliation evidence where applicable
- Content architecture/rendered/internal-link/SEO evidence where applicable
- Capability-quality baseline and post-P1 measurement when the catalog changed

## Findings

Record each finding with observed evidence, affected system/product boundary, failure or user-impact scenario, severity, required remediation, verification method, and residual limitation.

State `No findings` only after every applicable domain and mandatory evidence source has been inspected.

## Severity

Use the canonical ATLAS levels:

- Critical
- High
- Medium
- Low
- Note

Cross-tenant leakage, duplicate irreversible job effects, protected-cache leakage, production data-integrity failures, or fabricated/double-counted high-value business measurement are normally blocking until resolved or proven non-applicable.

## Review questions

### Database and tenancy

- Are important invariants enforced and migration-safe?
- Are indexes justified by query/workload evidence rather than habit?
- Can tenant data leak through storage, cache, jobs, search, export, analytics, logs, or support tooling outside RLS?
- Are pooled-resource noisy-neighbor and quota behaviors proportionate to risk?

### Jobs and caches

- Can duplicate/retried work repeat irreversible effects?
- Are retries bounded and poison work observable/recoverable?
- Can obsolete/cancelled work commit late?
- Are cache keys scoped to every representation-changing principal/variant?
- Can stale/shared cache preserve revoked authorization or cross-tenant state?

### Funnel and analytics

- Are friction findings evidence-backed or clearly hypotheses?
- Does the funnel's counted success correspond to downstream authoritative success?
- Can refresh/retry/client+server instrumentation double-count high-value events?
- Are identity, consent, PII, environment, and destination receipt handled deliberately?

### Content discoverability

- Can important content be reached and understood by people through intentional information architecture and links?
- Is important rendered content crawlable without interaction-only dependencies?
- Are technical SEO and structured-data responsibilities routed to existing dedicated skills?
- Are AI/search recommendations grounded in current official guidance rather than unsupported hacks or ranking promises?

### Capability health

- Did P1 add only skills unless a durable new responsibility was justified?
- Did post-P1 quality/routing/overlap metrics materially regress from the recorded baseline?

## Required actions

For every finding, specify the correction, decision, experiment, or evidence required and how it will be verified. Critical or High findings must be resolved or explicitly governed before approval. Missing cross-tenant, duplicate-job, protected-cache, authoritative-conversion, analytics-payload, or rendered-discoverability evidence must be listed as required action rather than assumed safe.

## Outcome

Record exactly one:

- Approved
- Approved with conditions
- Changes required
- Blocked

The sole implementer may provide evidence and remediation but must not be the only approver of significant P1 work.
