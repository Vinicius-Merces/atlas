# SaaS From Brief Delivery Workflow

## Trigger

A user asks ATLAS to create or materially expand a SaaS, authenticated business system, dashboard, marketplace, internal operational system, or AI-powered application from a brief.

## Objective

Compose a complete production SaaS from product intent through premium frontend, trustworthy data and identity boundaries, reusable operational primitives, failure handling, deployment, and independent evidence.

## Sequence

1. Decompose the brief into users, tenants, jobs-to-be-done, domain entities, invariants, revenue/entitlement model, integrations, and non-functional constraints.
2. Select a blueprint and architecture; define schema with `database-schema-review` and migration implications.
3. Establish authentication/authorization/multitenancy/RLS boundaries before building privileged UI.
4. Design CRUD/state transitions with `form-mutation-design` and tenant-safe files with `file-upload-storage-design` when required.
5. Add `application-search-design` and `data-import-export-workflow` for discovery/bulk-data jobs as applicable.
6. Design transactional communication with `transactional-email-delivery` and multi-channel state with `notification-system-design` where needed.
7. Add `rate-limit-abuse-control` to identity, public, AI, upload, search, export, messaging, and expensive provider paths according to risk.
8. Implement `audit-log-design` and `admin-operations-surface` for consequential support/privileged operations.
9. Use `feature-flag-rollout` for staged launches, migrations, experiments, or kill switches when rollout risk warrants it.
10. Compose background jobs, caching, webhooks, payments, external API resilience, observability, and reconciliation as the product requires.
11. Build every user-facing surface under Frontend Craft, including dashboard/admin forms, tables, empty/error/loading states and responsive behavior.
12. Run SaaS Production Trust, P1 Production/Product Quality, browser/assurance, security, performance and supply-chain gates.
13. Complete independent `full-stack-delivery-review` before production approval.

## Responsible agents

- `orchestrator` / `solution-blueprint-engineer`: compose the capability path without redundant personas.
- `product-architect` / `product-manager`: domain and product authority.
- `frontend-engineer` / `ux-director`: premium interaction and information design.
- `backend-engineer` / `data-engineer`: authoritative state and data primitives.
- `integration-engineer` / `platform-engineer` / `reliability-engineer`: providers, jobs, delivery and operations.
- `security-engineer` / `qa-engineer`: independent trust and behavior evidence.

## Validation

- Prove primary authenticated journeys and at least one negative/failure state per material primitive.
- Test horizontal, vertical and cross-tenant boundaries across database, files, search, notifications, exports and admin surfaces.
- Exercise duplicate mutation/job/provider events, stale state, retry/recovery, flag rollback and privileged audit evidence where applicable.
- Validate representative phone/tablet/desktop UI, accessibility, performance and browser behavior.
- Reconcile payments/entitlements, imports/exports, notifications, files, search indexes or provider state when architecture permits divergence.

## Completion criteria

The SaaS has explicit authoritative state, tenant/user isolation across all shared subsystems, governed delivery primitives, premium frontend evidence, reliable failure/recovery paths, deployable configuration, and independent review approval.
