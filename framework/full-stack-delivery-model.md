# ATLAS Full-Stack Delivery Model

## Purpose

The Full-Stack Delivery model turns ATLAS from a strong review framework into a composable production-construction system for premium websites and SaaS products.

The governing chain is:

**brief → product intent → architecture → authoritative data → delivery primitives → premium frontend → trust boundaries → browser/production evidence → independent review**

A project is not complete because pages render or CRUD works. Delivery is complete when the product can create and mutate state safely, communicate with users, operate privileged workflows, handle files and bulk data, expose useful search/content, roll out change safely, and preserve the Frontend Craft, SaaS Production Trust, Web Production Assurance, and P1 quality gates that apply.

## Construction principles

1. **Compose capabilities, do not clone personas.** Existing durable agents own the new primitives.
2. **Authority before UI optimism.** Every mutation, notification, export, flag, and audit event names its authoritative state.
3. **Premium is a system quality.** Typography, composition, motion, responsive behavior, accessibility, performance, forms, empty/error states, and operational UX all participate.
4. **Provider features are implementation tools.** Storage, email, CMS, search, flags, and queues do not replace application contracts.
5. **Failure paths are product paths.** Duplicate submission, provider outage, stale index, failed upload, partial import, disabled flag, and admin denial are designed deliberately.
6. **Privileged and tenant boundaries survive every subsystem.** Search, files, notifications, exports, admin tools, caches, queues, and audit records remain tenant/user scoped.
7. **Every reusable primitive owns cleanup.** Files, flags, notifications, imports, exports, audit retention, and content schema migrations have lifecycle rules.

## Primitive families

### State and data interaction

- `form-mutation-design`
- `file-upload-storage-design`
- `application-search-design`
- `data-import-export-workflow`

### Communication and operations

- `transactional-email-delivery`
- `notification-system-design`
- `audit-log-design`
- `admin-operations-surface`

### Product delivery controls

- `rate-limit-abuse-control`
- `feature-flag-rollout`
- `cms-content-modeling`

## Website composition

A public website starts with product/brand intent and Frontend Craft. Add `cms-content-modeling` when editors own content, `form-mutation-design` for lead/contact/booking interactions, `file-upload-storage-design` for user/media uploads, and `application-search-design` when discovery is part of the user job. Public releases preserve accessibility, responsive, performance, browser, SEO, structured-data, analytics, conversion, and supply-chain gates.

## SaaS composition

A SaaS adds authenticated mutations, tenant-safe files/search/import-export, transactional communication, notification state, rate/resource controls, audit evidence, admin/support operations, and staged rollout as applicable. These compose with authentication, authorization, RLS, multitenancy, schema, jobs, caching, payments, webhooks, external APIs, analytics, observability, and recovery.

## Premium frontend invariants

Every user-facing blueprint inherits Frontend Craft. Significant UI work requires a visual thesis, deliberate stack choice, design-system consistency, accessible interactions, responsive evidence, visual regression review, web-performance readiness, browser validation, and independent craft approval. Admin tools and SaaS dashboards are not exempt because they are less marketing-oriented.

## Technology admission

Choose the smallest technology that satisfies the contract. A database may be enough for search before a dedicated engine; direct object storage may use scoped signed authorization; queues are justified by duration/reliability needs; CMS/flag providers are selected by editorial/rollout requirements rather than fashion.

Current assurance anchors include OWASP resource-consumption controls, provider-scoped signed object access patterns, current PostgreSQL full-text search capabilities, and vendor-neutral feature-flag evaluation-context principles. ATLAS guidance remains provider neutral and must verify selected provider semantics during implementation.

## Completion standard

A site or SaaS can be called production-ready only when applicable primitives are implemented or explicitly not applicable, authoritative state and tenant/user boundaries are clear, critical negative paths are exercised, premium frontend gates pass, deployment/runtime evidence exists, and `.claude/reviews/full-stack-delivery-review.md` reaches an acceptable outcome.
