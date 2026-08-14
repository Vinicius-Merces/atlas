# SaaS From Brief Delivery Workflow

## Trigger

A user asks ATLAS to create or materially expand a SaaS, authenticated business system, dashboard, marketplace, internal operational system, or AI-powered application from a brief.

## Objective

Compose a complete production SaaS from product intent through premium frontend, trustworthy data and identity boundaries, reusable operational primitives, failure handling, deployment, and independent evidence.

## Inputs

- Product brief, users, tenant/account model, jobs-to-be-done, acceptance criteria, business rules, and non-functional constraints.
- Revenue, subscription, entitlement, or internal permission model where applicable.
- Existing architecture, schema, integrations, providers, deployment/runtime, and migration constraints for non-greenfield work.
- Data sensitivity, privacy/compliance requirements, expected scale, availability, performance, and operational support needs.
- Brand/design direction plus representative target devices and browsers.

## Sequence

1. Decompose the brief into users, tenants, jobs-to-be-done, domain entities, invariants, revenue/entitlement model, integrations, and non-functional constraints.
2. Select a blueprint and architecture; define schema with `database-schema-review` and migration implications.
3. Establish authentication/authorization/multitenancy/RLS boundaries before building privileged UI.
4. Design CRUD/state transitions with `form-mutation-design` and tenant-safe files with `file-upload-storage-design` when required.
5. Add `application-search-design` and `data-import-export-workflow` for discovery/bulk-data jobs as applicable. Run `cms-content-modeling` when editor-owned product, help, marketing, listing, or documentation content must publish independently from code.
6. Design transactional communication with `transactional-email-delivery` and multi-channel state with `notification-system-design` where needed.
7. Add `rate-limit-abuse-control` to identity, public, AI, upload, search, export, messaging, and expensive provider paths according to risk.
8. Implement `audit-log-design` and `admin-operations-surface` for consequential support/privileged operations.
9. Use `feature-flag-rollout` for staged launches, migrations, experiments, or kill switches when rollout risk warrants it.
10. Compose background jobs, caching, webhooks, payments, external API resilience, observability, and reconciliation as the product requires.
11. Before UI implementation, run `interface-visual-direction`. When the brief asks for premium or non-vibe-coded quality, freeze the Frontend Craft premium delivery contract: product vocabulary, visual thesis, signature moment, justified aesthetic risk, token grammar, motion/state inventory, responsive recomposition, and screenshot acceptance matrix. Then build every user-facing surface under Frontend Craft, including dashboard/admin forms, tables, empty/error/loading/success/destructive states and responsive behavior.
12. Run SaaS Production Trust, P1 Production/Product Quality, browser/assurance, security, performance and supply-chain gates.
13. Complete independent `full-stack-delivery-review` before production approval.

## Required lifecycle

1. **Understand** - Resolve actors, tenants, domain invariants, authoritative state, revenue/entitlements, integrations, operational ownership, constraints, and success criteria.
2. **Inspect** - Read existing code/schema/runtime/provider behavior and prior trust/quality evidence when present.
3. **Plan** - Select blueprint, architecture, schema/migrations, identity/tenant model, applicable P2 primitives, frontend thesis, failure/recovery paths, observability, and release strategy.
4. **Execute** - Build incrementally with server-authoritative privileged state, tenant-safe resources, reliable distributed transitions, and premium frontend composition.
5. **Validate** - Exercise positive, denial, duplicate, concurrent, cross-tenant, stale, retry, provider-outage, privileged, responsive, accessibility, performance, and browser paths as applicable.
6. **Review** - Complete independent trust, P1 quality, frontend/web assurance, security, and Full-Stack Delivery gates appropriate to scope.
7. **Document** - Record domain/architecture decisions, provider contracts, operational procedures, rollout/rollback, recovery, evidence, and residual risks.
8. **Deliver** - Release only when blocking findings are resolved and production configuration/runtime behavior is verified.

## Responsible agents

- `orchestrator` / `solution-blueprint-engineer`: compose the capability path without redundant personas.
- `product-architect` / `product-manager`: domain and product authority.
- `frontend-engineer` / `ux-director`: premium interaction and information design.
- `backend-engineer` / `data-engineer`: authoritative state and data primitives.
- `integration-engineer` / `platform-engineer` / `reliability-engineer`: providers, jobs, delivery and operations.
- `security-engineer` / `qa-engineer`: independent trust and behavior evidence.

## Decision points

- What is the authoritative source for each consequential business state and who may change it?
- Where is tenant identity established, propagated, enforced, cached, indexed, queued, stored, exported, and observed?
- Which P2 primitives are required and which are genuinely not applicable?
- Does a CMS, dedicated search engine, queue, external notification provider, feature-flag service, or other dependency solve a demonstrated requirement?
- Which mutations/jobs/provider calls can be duplicated, reordered, retried, or become obsolete?
- Which privileged operations need confirmation, re-authentication, reason capture, dual control, break-glass, or audit evidence?
- What makes the frontend premium for this product category without importing marketing-site theatrics into operational UX?
- What product-specific command surface or interaction prevents the first authenticated viewport from collapsing into a generic sidebar/cards/table shell?
- What metrics and failure thresholds trigger rollback or degraded mode?

## Validation

- Prove primary authenticated journeys and at least one negative/failure state per material primitive.
- Test horizontal, vertical and cross-tenant boundaries across database, files, search, notifications, exports and admin surfaces.
- Exercise duplicate mutation/job/provider events, stale state, retry/recovery, flag rollback and privileged audit evidence where applicable.
- Validate representative phone/tablet/desktop UI, accessibility, performance and browser behavior.
- Treat build success and source inspection as insufficient for visual approval; compare rendered evidence against the frozen frontend direction and interaction-state matrix.
- Reconcile payments/entitlements, imports/exports, notifications, files, search indexes or provider state when architecture permits divergence.

## Failure handling

- Do not infer tenant, role, entitlement, retention, billing, or support policy from incidental implementation state.
- Do not rely on hidden UI, feature flags, storage paths, cache keys, search filtering, or notification routing as substitutes for authorization.
- Do not accept irreversible duplicate effects because a provider/queue is expected to deliver once.
- Do not declare distributed integration success solely from an intermediate provider response when authoritative state can diverge.
- Do not let privileged support/admin actions bypass domain invariants or become unaudited direct-database workflows by default.
- If a dependency is unavailable, follow explicit degradation/retry/reconciliation policy rather than silently losing state.
- If required trust/browser/frontend evidence is unavailable, report the claim as unverified and block release when material.

## Completion criteria

The SaaS has explicit authoritative state, tenant/user isolation across all shared subsystems, governed delivery primitives, premium frontend evidence, reliable failure/recovery paths, deployable configuration, and independent review approval.
