# Production Systems & Product Quality Model

ATLAS P1 extends the completed P0 foundation into two connected pillars:

1. **Production systems quality** — schema integrity, multitenancy beyond database policy, background-job reliability, and deliberate cache consistency.
2. **Product/growth quality** — conversion funnels, trustworthy analytics implementation, and content discoverability for humans, search, and AI-assisted discovery.

The model is vendor-neutral. Provider features implement parts of these controls but do not replace application responsibility.

## Relationship to existing ATLAS models

P1 composes with, rather than duplicates:

- Frontend Craft for authored visual/responsive/performance quality;
- SaaS Production Trust for authentication, authorization, RLS, secrets, webhooks, payments, and external APIs;
- Web Production Assurance for real-browser behavior, technical SEO, structured-data truth, and supply-chain risk;
- Capability Evaluation for measured catalog quality and role-boundary discipline.

## Production systems pillar

### Database schema integrity

Schemas are executable integrity contracts. Prefer database-enforced invariants when practical, but judge constraints and indexes against real domain and query behavior. Indexes accelerate reads at storage/write/maintenance cost, so existence alone is not quality.

High-risk schema changes require migration/backfill/coexistence reasoning, not only a correct final-state model.

### Multitenancy beyond RLS

Tenant isolation spans identity, application authorization, database policy, object storage, caches, jobs, search/vector indexes, analytics, exports, observability, quotas, and support operations.

Pooled infrastructure creates shared efficiency and shared blast radius. Noisy-neighbor controls, tenant-aware attribution, quotas, and per-tenant admission are part of production correctness where resources are shared.

### Background work

Treat asynchronous delivery as repeatable unless the whole provider/application contract proves stronger semantics. Even systems designed to minimize duplicates can execute work more than once under rare failure conditions.

Business side effects therefore need idempotency, bounded retries, observable dead-letter/replay behavior, cancellation/obsolescence rules, and reconciliation for ambiguous outcomes.

### Cache consistency

Caching is an optimization and resilience tool, not an authority layer. Every cache needs an explicit objective, source of truth, key scope, freshness model, invalidation/revalidation path, and safe degradation behavior.

Private/user/tenant-sensitive responses must not cross principal boundaries through shared keys or caches. Stale serving must never silently preserve revoked authorization or other correctness-critical security state.

## Product and growth pillar

### Conversion quality

Conversion is a product outcome, not a reason to manipulate users. Funnel review connects acquisition, information clarity, form effort, technical failures, downstream handoff, lead/customer quality, and measurement.

Optimization hypotheses remain hypotheses until supported by observational evidence or controlled experiments. Short-term conversion lift must be weighed against trust, retention, fraud/abuse, support cost, accessibility, and downstream quality.

### Analytics trust

An analytics implementation is trustworthy only when event semantics, properties, identity, consent, deduplication, environment separation, and destination receipt match the canonical measurement model.

Client and server collection can complement each other but can also double-count. High-value events such as purchase, signup, lead, or activation should be tied to authoritative application state and reconciled where feasible.

### Content discoverability

Content architecture should make important information easy to find and understand for people first, while remaining crawlable and technically accessible to search/AI discovery systems.

ATLAS rejects special “AI SEO” hacks presented without evidence. Current major search guidance continues to emphasize the same crawlability, useful people-first content, technical SEO, JavaScript/rendering, page experience, and semantic/accessibility fundamentals for AI-assisted search experiences.

## P1 operating sequence

For a material P1 change:

1. identify authoritative data/product state;
2. classify applicable P1 domains;
3. run the closest focused skills;
4. compose with P0 trust/web/frontend gates where boundaries intersect;
5. validate failure, cross-tenant, stale, duplicate, measurement, and rendered paths proportionally to risk;
6. complete independent production/product-quality review;
7. re-run Capability Evaluation when the capability catalog itself changes.

## Blocking examples

Normally block approval when evidence shows:

- invalid or orphanable production data that should be prevented by schema/invariant design;
- cross-tenant leakage through storage, cache, job, search, export, analytics, or support paths;
- duplicate asynchronous execution causing irreversible business effects;
- stale/shared cache serving protected data across authorization or tenant boundaries;
- high-value analytics events double-counting or reporting fabricated business state;
- conversion tactics that are deceptive or violate required consent/accessibility boundaries;
- discoverability recommendations that fabricate content/entities or promise rankings/AI inclusion without evidence.

## Capability-evaluation requirement

P1 was admitted only after the pre-P1 baseline measured all registered skills and all 87 agent surfaces and found no agent pair at or above the overlap review threshold. P1 therefore adds skills only, not new specialist agents.

After P1 is implemented, rerun the same quality/routing/overlap metrics and compare them with `docs/assurance/capability-quality-baseline-2026-08-13.md`.
