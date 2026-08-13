# Production Systems & Product Quality Readiness Workflow

## Trigger

A feature or release materially changes database structure, multi-tenant resource behavior, queues/background work, caching, conversion/activation flows, analytics instrumentation, or content information architecture/discoverability.

## Objective

Deliver production and product changes whose data integrity, tenant isolation, asynchronous reliability, cache consistency, measurement trust, funnel behavior, and content discoverability are explicitly validated using applicable P1 capabilities and existing P0 trust/web gates.

## Inputs

- Product request, acceptance criteria, risk, and authoritative business state
- Current architecture, schemas, migrations, tenant/resource model, queues, caches, and providers
- Funnel/user journey and downstream handoff state
- Analytics taxonomy, implementation, privacy/consent requirements, and destination evidence
- Content inventory, information architecture, rendering, SEO, and structured-data evidence
- Pre-P1 capability-quality baseline

## Sequence

1. **Classify the P1 surface**
   - Read `framework/production-product-quality-model.md`.
   - Identify production-system and product/growth domains that actually changed.

2. **Review schema integrity when applicable**
   - Run `database-schema-review` for relational schema/invariant/index/lifecycle changes.
   - Compose with `database-migration-analysis` for material migration/backfill risk.

3. **Review multitenancy when applicable**
   - Run `saas-multitenancy-review` when tenant identity or shared/siloed resources change.
   - Preserve P0 `authorization-boundary-review` and `row-level-security-review` where relevant.

4. **Review asynchronous reliability when applicable**
   - Run `background-job-reliability` for queues, workers, scheduling, retries, duplicate execution, or dead-letter/replay behavior.

5. **Assess caching when applicable**
   - Run `cache-strategy-assessment` for browser/CDN/edge/server/distributed cache behavior, especially tenant or authorization-sensitive state.

6. **Review conversion quality when applicable**
   - Run `conversion-funnel-review` for acquisition, onboarding, forms, activation, checkout, or handoff changes.
   - Use browser and experiment evidence proportionally to uncertainty.

7. **Audit analytics implementation when applicable**
   - Run `analytics-implementation-audit` whenever funnel/KPI conclusions rely on changed instrumentation.
   - Reconcile high-value events against authoritative product/business state where feasible.

8. **Review content discoverability when applicable**
   - Run `content-discoverability-review` for information architecture, internal linking, semantic/rendered content, or search/AI-discovery changes.
   - Compose with `seo-technical-audit` and `structured-data-validation` for technical signals.

9. **Run cross-domain failure validation**
   - Exercise cross-tenant, duplicate/retry, stale/invalidation, migration, measurement duplication, browser error/recovery, and rendered discoverability paths as applicable.

10. **Complete independent review**
   - Run `.claude/reviews/production-product-quality-review.md` with a reviewer who was not the sole implementer.

11. **Re-measure capability quality when the catalog changed**
   - Run the Capability Evaluation pack and compare against the pre-P1 baseline.

## Required lifecycle

1. **Understand** - Define user/business outcomes, authoritative state, tenancy, data sensitivity, measurement needs, and content intent.
2. **Inspect** - Read current schemas, jobs, caches, analytics, content architecture, P0 trust evidence, and capability baseline.
3. **Plan** - Select only applicable P1 skills, negative/failure checks, review ownership, observability, and rollback/recovery.
4. **Execute** - Implement incrementally with strong invariants, tenant-safe keys/state, idempotency, bounded caching, honest measurement, and people-first content.
5. **Validate** - Run representative positive, negative, duplicate, stale, cross-tenant, analytics, browser, and migration checks.
6. **Review** - Complete independent P1 and applicable P0 review gates.
7. **Document** - Record evidence, authoritative sources, residual risk, measurement limits, and durable architecture/memory changes.
8. **Deliver** - Report Approved, Approved with conditions, Changes required, or Blocked based on evidence.

## Responsible agents

- `orchestrator`: route P1 capabilities without adding redundant agents.
- `backend-engineer` / `data-engineer`: primary schema, multitenancy data path, job, and cache implementation owners as assigned.
- `reliability-engineer` / `platform-engineer`: shared-resource, queue, cache, capacity, and recovery owners as assigned.
- `security-engineer`: cross-tenant and authorization boundary reviewer where trust is affected.
- `product-manager` / `ux-director` / `content-designer`: product/funnel/content intent owners as assigned.
- `analytics-engineer` / `experimentation-analyst`: measurement and causal-evidence owners.
- `qa-engineer` or another independent reviewer: validates critical behavior and evidence.

## Decision points

- Which P1 domains actually changed and which are not applicable?
- What state is authoritative for schema, tenant, job, cache, conversion, analytics, and content decisions?
- Can a tenant/resource/user boundary be crossed outside the database?
- Can a job run twice or finish after it becomes obsolete?
- Can cached state remain valid after authorization, tenant, locale, content, or business-state mutation?
- Is a funnel conclusion measured, inferred, or an experiment hypothesis?
- Do analytics events correspond to real authoritative business state?
- Does content discoverability improve human access as well as machine discovery?
- Did P1 degrade skill routing quality or agent-boundary clarity versus baseline?

## Validation

- Run every applicable focused P1 skill and its required evidence checks.
- Preserve P0 trust/web/frontend gates where boundaries intersect.
- Execute representative schema invariant and migration checks for material database changes.
- Execute cross-tenant tests beyond RLS when shared resources exist.
- Test duplicate/retry/timeout/dead-letter paths for material background jobs.
- Test cache hit/miss/stale/invalidation and protected-key scope where caching matters.
- Validate primary conversion flow in a browser and verify downstream success state.
- Inspect actual analytics payloads/destination receipt and duplication behavior.
- Inspect rendered/internal-link/content paths for discoverability changes.
- Re-run `evaluate_skill_quality.py`, `evaluate_skill_routing.py`, and `analyze_agent_overlap.py` when P1 changes the capability catalog.

## Failure handling

- Do not infer missing product permission, tenant, retention, or KPI policy from implementation accidents.
- Do not accept duplicate irreversible job effects because the queue is described as reliable.
- Do not cache protected state across user/tenant boundaries or serve stale revoked authorization for availability.
- Do not count a UI success page as authoritative conversion/payment/activation state when downstream state failed.
- Do not rewrite analytics taxonomy merely to match accidental instrumentation.
- Do not create keyword/AI-targeted content that has no user information value.
- Do not add a new agent to resolve a procedural gap unless overlap analysis and durable ownership justify it.

## Completion criteria

- Applicable P1 domains are completed or marked not applicable with architectural reason.
- Data invariants, tenant resources, jobs, and caches have explicit authority/failure models where changed.
- Conversion and analytics findings distinguish evidence from hypotheses.
- Discoverability recommendations preserve people-first useful content and technical truth.
- Applicable P0 gates remain satisfied.
- Independent P1 review is Approved or Approved with resolved/governed conditions.
- Post-P1 capability metrics are recorded and compared with the pre-P1 baseline.
