# Skill Catalog

Canonical, generated inventory of every skill under `.claude/skills/<skill-name>/SKILL.md`. Each entry mirrors its frontmatter `description`, which is the routing and discovery summary used by AI runtimes.

Regenerate both capability catalogs with `python scripts/generate_capability_catalogs.py`. Use `--check` in validation and CI.

Total: 128 skills.

## Accessibility Audit

`accessibility-audit`. Review user-facing work for common accessibility failures.

## Adapter Drift Detection

`adapter-drift-detection`. Detect divergence between a supported runtime adapter and canonical ATLAS.

## Admin Operations Surface

`admin-operations-surface`. Design privileged admin/support surfaces with least-privilege roles, explicit tenant context, safe search, impersonation controls, dangerous-action confirmation, audit evidence, and break-glass access.

## ADR Authoring

`adr-authoring`. Capture an important architecture decision with sufficient context and traceability.

## Agent Overlap Analysis

`agent-overlap-analysis`. Measure semantic overlap across registered ATLAS agents when roles are added, scopes change, or the catalog may contain redundant responsibilities, using descriptions, missions, ownership, and taxonomy boundaries.

## AI System Design

`ai-system-design`. Design an AI-enabled system with explicit capabilities, limitations, data flow, and evaluation.

## Analytics Implementation Audit

`analytics-implementation-audit`. Audit product analytics implementation when events, properties, identity, consent, ecommerce, client/server collection, destinations, or decision metrics change, verifying taxonomy parity and trustworthy measurement.

## API Contract Analysis

`api-contract-analysis`. Assess API compatibility and identify migration risks.

## Application Search Design

`application-search-design`. Design product/content search with source-of-truth fields, query semantics, ranking, filters, pagination, indexing, authorization, tenant scope, freshness, failure states, and database-versus-search-engine tradeoffs.

## Ai Search Measurement

`ai-search-measurement`. Establish and interpret AI-search/GEO measurement using reproducible query sets, Search Console/analytics evidence, attribution limits, and explicit confounders.

## Architecture Assessment

`architecture-assessment`. Evaluate whether a proposed change fits existing architecture and preserves clear boundaries.

## Architecture Audit

`architecture-audit`. Audit architecture for clarity, ownership, coupling, resilience, and alignment.

## Architecture Portfolio Assessment

`architecture-portfolio-assessment`. Assess multiple systems as a portfolio rather than isolated architectures.

## Audit Bundle Assembly

`audit-bundle-assembly`. Assemble a navigable manifest of evidence for a task, release, or deployment.

## Audit Log Design

`audit-log-design`. Design audit logs for consequential actions with actor, tenant, resource, action/result, correlation, sensitive-data minimization, integrity expectations, retention, access control, export, and investigation usability.

## Authentication Flow Review

`authentication-flow-review`. Review sign-in, sign-up, recovery, MFA, SSO/OAuth/OIDC, session creation, and account-linking flows when identity behavior changes or authentication must be production-ready.

## Authorization Boundary Review

`authorization-boundary-review`. Review resource and action permissions when roles, ownership, tenants, admin paths, APIs, or privileged operations change, verifying deny-by-default authorization at every trust boundary.

## Background Job Reliability

`background-job-reliability`. Review background jobs and queues when asynchronous work, retries, scheduling, concurrency, leases, deduplication, cancellation, dead letters, or worker recovery change, assuming duplicate delivery can occur.

## Blueprint Selection

`blueprint-selection`. Choose the closest ATLAS blueprint for a project.

## Browser Flow Validation

`browser-flow-validation`. Validate critical user journeys in a real browser when releases or frontend changes need evidence for navigation, forms, auth states, errors, console/network failures, and cross-viewport behavior.

## Cache Strategy Assessment

`cache-strategy-assessment`. Assess caching when browser, CDN, edge, server, database, runtime, or distributed caches change, verifying key scope, freshness, invalidation, authorization safety, stampede control, and consistency tradeoffs.

## Change Provenance Mapping

`change-provenance-mapping`. Map file changes to tasks, decisions, runtimes, validation, and reviews.

## Cloud Cost Analysis

`cloud-cost-analysis`. Analyze cloud or platform spending and identify evidence-based optimization opportunities.

## Cms Content Modeling

`cms-content-modeling`. Design CMS content models and editorial workflows with structured types, slugs, drafts, preview, localization, media, publishing lifecycle, references, SEO fields, migrations, and frontend rendering contracts.

## Codex Runtime Generation

`codex-runtime-generation`. Generate or synchronize the Codex adapter from canonical ATLAS definitions.

## Command Catalog Synthesis

`command-catalog-synthesis`. Produce a runtime-oriented catalog of all canonical ATLAS commands.

## Compatibility Matrix Analysis

`compatibility-matrix-analysis`. Evaluate compatibility across framework versions, runtimes, adapters, and project states.

## Compliance Evidence Mapping

`compliance-evidence-mapping`. Map requirements to controls, implementation evidence, and ownership.

## Component Reuse Assessment

`component-reuse-assessment`. Determine whether an existing frontend component should be reused, extended, or replaced.

## Conflict Prediction

`conflict-prediction`. Predict overlapping changes and dependency conflicts before parallel execution.

## Content Discoverability Review

`content-discoverability-review`. Review content discoverability when information architecture, internal links, semantic structure, rendering, topic/entity organization, or AI/search visibility changes, aligning human navigation with crawlable authoritative content.

## Content Quality Review

`content-quality-review`. Review product copy for clarity, consistency, actionability, and audience fit.

## Context Pack Composition

`context-pack-composition`. Assemble relevant project context while preserving sources and excluding secrets.

## Continuation Planning

`continuation-planning`. Create an ordered continuation plan from a validated handoff.

## Continuity Reconciliation

`continuity-reconciliation`. Reconcile project briefs, session briefs, resume packets, tasks, checkpoints, and repository state.

## Control Design

`control-design`. Design a proportionate preventive, detective, or corrective control.

## Conversion Funnel Review

`conversion-funnel-review`. Review conversion funnels when acquisition, landing pages, forms, onboarding, checkout, lead handoff, or activation paths change, connecting user friction and measurement to business outcomes without dark patterns.

## Core Contract Stabilization

`core-contract-stabilization`. Evaluate whether a contract is stable enough for a beta support commitment.

## Data Import Export Workflow

`data-import-export-workflow`. Design bulk data import/export with authorization, schema mapping, preview, validation, partial errors, idempotency, background processing, progress, large-file handling, privacy, and secure artifact lifecycle.

## Database Migration Analysis

`database-migration-analysis`. Assess schema and data migrations for integrity, compatibility, and operational risk.

## Database Schema Review

`database-schema-review`. Review relational database schema changes when tables, columns, constraints, indexes, relationships, partitioning, retention, or migration-sensitive data models change, verifying integrity and query-fit before release.

## Dependency Graph Analysis

`dependency-graph-analysis`. Analyze dependency direction, cycles, coupling, and change impact.

## Dependency Impact Analysis

`dependency-impact-analysis`. Evaluate the risk and value of adding or upgrading a dependency.

## Deprecation Planning

`deprecation-planning`. Plan a safe deprecation and removal lifecycle.

## Design Token Architecture

`design-token-architecture`. Design semantic, scalable tokens for multi-theme and multi-platform products.

## Developer Onboarding Assessment

`developer-onboarding-assessment`. Evaluate whether a new contributor can understand, run, test, and modify the project reliably.

## Documentation Information Architecture

`documentation-information-architecture`. Organize documentation around user needs, canonical concepts, and lifecycle.

## Dual Runtime Validation

`dual-runtime-validation`. Validate Claude Code and Codex runtime support in the same release.

## Entity Authority Mapping

`entity-authority-mapping`. Map public entities, factual claims, evidence owners, canonical sources, and conflicts before GEO, schema, knowledge-content, or AI-search work.

## Event Taxonomy Design

`event-taxonomy-design`. Design stable, privacy-aware analytics events and properties.

## Evidence Record Design

`evidence-record-design`. Create a portable evidence record for a task or workstream.

## Execution Checkpointing

`execution-checkpointing`. Capture immutable execution state at a meaningful task boundary.

## Experiment Design

`experiment-design`. Design an experiment with explicit hypothesis, metrics, population, analysis, and decision rules.

## External API Resilience Review

`external-api-resilience-review`. Review third-party API integrations when timeouts, retries, rate limits, pagination, versioning, partial failures, provider outages, or fallback behavior can affect production reliability.

## Feature Flag Rollout

`feature-flag-rollout`. Design feature flags and staged rollouts by environment, user, tenant, cohort, percentage, or kill switch with trusted evaluation context, safe defaults, metrics, rollback, lifecycle ownership, and flag removal.

## File Upload Storage Design

`file-upload-storage-design`. Design file upload and object-storage flows with ownership, authorization, signed access, type/size validation, safe object keys, integrity, processing, retention, deletion, and tenant isolation.

## Form Mutation Design

`form-mutation-design`. Design user-initiated forms and state mutations with server validation, authorization, duplicate-submit safety, concurrency, optimistic UI, failure recovery, revalidation, and accessible feedback.

## Framework Package Validation

`framework-package-validation`. Verify that an ATLAS distribution is structurally complete and internally consistent.

## Frontend Craft Review

`frontend-craft-review`. Independently review a frontend for visual craft and anti-template quality when implementation is functionally complete but must not look generic, derivative, or AI-default.

## Frontend Stack Selection

`frontend-stack-selection`. Select frontend libraries and rendering tools when a user-facing web change needs implementation or modernization, choosing CSS, Motion, GSAP, React Three Fiber, primitives, and supporting libraries by evidence rather than trend.

## Immersive 3D Experience

`immersive-3d-experience`. Design and review web 3D with Three.js or React Three Fiber when spatial interaction or narrative depth is justified, with strict performance, fallback, and accessibility budgets.

## Incident Triage

`incident-triage`. Rapidly classify and stabilize a production incident.

## Incremental Patch Verification

`incremental-patch-verification`. Verify patch base version, file hashes, replacements, additions, and deletions before application.

## Infrastructure Change Assessment

`infrastructure-change-assessment`. Evaluate the operational risk of infrastructure or deployment changes.

## Integration Contract Mapping

`integration-contract-mapping`. Document the complete behavioral and operational contract of an integration.

## Interface Visual Direction

`interface-visual-direction`. Define a distinctive visual direction before implementation when a user-facing surface needs premium hierarchy, composition, typography, rhythm, imagery, depth, and interaction intent.

## Knowledge Graph Synthesis

`knowledge-graph-synthesis`. Convert distributed project documents into a linked and traceable knowledge structure.

## Localization Readiness Assessment

`localization-readiness-assessment`. Assess whether a product or feature is structurally ready for translation and locale variation.

## Manual Deployment Preflight

`manual-deployment-preflight`. Validate an incremental package before files are copied manually.

## Manual Deployment Receipt

`manual-deployment-receipt`. Record a manually applied patch without requiring deployment automation.

## Memory Drift Analysis

`memory-drift-analysis`. Compare durable memory and continuity artifacts against current repository evidence.

## Memory Freshness Audit

`memory-freshness-audit`. Assess persistent memory ownership, source, age, and reliability.

## Memory Update Proposal

`memory-update-proposal`. Produce a reviewable proposal instead of silently rewriting durable memory.

## Mobile Architecture Assessment

`mobile-architecture-assessment`. Evaluate mobile architecture for platform fit, maintainability, offline behavior, performance, and release constraints.

## Motion Choreography

`motion-choreography`. Design and implement purposeful UI motion when a frontend needs transitions, gestures, scroll choreography, or timelines, selecting CSS, Motion, or GSAP by interaction semantics.

## Notification System Design

`notification-system-design`. Design in-app, push, email, or provider notifications with trusted recipient rules, preferences, deduplication, urgency, read state, fan-out, retries, quieting, and accessible notification-center UX.

## Observability Design

`observability-design`. Design logs, metrics, traces, dashboards, and alerts for a feature or service.

## Payment Integration Review

`payment-integration-review`. Review payment and billing integrations when checkout, subscriptions, invoices, refunds, entitlements, webhooks, idempotency, or provider state synchronization change.

## Performance Budget Analysis

`performance-budget-analysis`. Define and evaluate measurable performance limits.

## Policy As Code Design

`policy-as-code-design`. Translate a stable governance rule into an executable and reviewable policy.

## Policy Exception Handling

`policy-exception-handling`. Create and review scoped, temporary policy exceptions.

## Policy Rule Design

`policy-rule-design`. Define policy conditions, severity, evidence, remediation, and enforcement outcome.

## Privacy Impact Assessment

`privacy-impact-assessment`. Identify privacy risks created by a feature, integration, or data flow.

## Product Requirement Decomposition

`product-requirement-decomposition`. Convert a broad product request into explicit outcomes, constraints, scope, and acceptance criteria.

## Project Adoption Assessment

`project-adoption-assessment`. Determine which ATLAS capabilities should be introduced into a project.

## Project Brief Synthesis

`project-brief-synthesis`. Create a compact project brief from canonical memory, architecture, decisions, runtime state, and documentation.

## Project Health Assessment

`project-health-assessment`. Assess a project's technical and operational health using consistent evidence.

## Prompt Model Evaluation

`prompt-model-evaluation`. Compare prompt, model, retrieval, or tool configurations using repeatable evaluation scenarios.

## RAG Architecture Assessment

`rag-architecture-assessment`. Evaluate retrieval-augmented generation architecture for grounding, security, freshness, quality, latency, and cost.

## Rate Limit Abuse Control

`rate-limit-abuse-control`. Design abuse and resource controls for public or expensive operations using actor-aware rate/concurrency limits, payload bounds, OTP/recovery protections, provider-spend controls, bypass policy, and observability.

## Reference Implementation Review

`reference-implementation-review`. Assess whether a reference project demonstrates ATLAS correctly.

## Registry To Runtime Generation

`registry-to-runtime-generation`. Generate runtime catalogs and indexes from the canonical ATLAS registry.

## Regression Risk Analysis

`regression-risk-analysis`. Estimate the likelihood and impact of regressions before implementation or release.

## Release Integrity Verification

`release-integrity-verification`. Verify that a release artifact is complete, consistent, and traceable.

## Repository Mapping

`repository-mapping`. Create a reliable structural map of an unfamiliar repository.

## Resource Claim Design

`resource-claim-design`. Declare file, directory, schema, service, and knowledge claims for a workstream.

## Responsive Layout Audit

`responsive-layout-audit`. Audit responsive composition across viewport and container sizes when user-facing layouts must remain intentional rather than merely stacking on smaller screens.

## Result Reconciliation

`result-reconciliation`. Combine validated workstream outputs into one coherent task result.

## Resume Packet Assembly

`resume-packet-assembly`. Assemble a bounded repository-native packet for cross-session or cross-runtime continuation.

## Row Level Security Review

`row-level-security-review`. Review PostgreSQL/Supabase row-level security when exposed tables, tenancy, ownership policies, service roles, views, or database authorization change, verifying default-deny data isolation.

## Runtime Adapter Mapping

`runtime-adapter-mapping`. Map canonical ATLAS capabilities to a target AI coding runtime.

## Runtime Conformance Testing

`runtime-conformance-testing`. Test runtime declarations, capabilities, shared sources, workflows, reviews, and evidence.

## Runtime Execution Planning

`runtime-execution-planning`. Create an execution plan from a task envelope, context pack, runtime declaration, workflow, and reviews.

## Runtime Handoff Design

`runtime-handoff-design`. Build a portable handoff manifest between supported runtimes.

## Runtime Semantic Parity

`runtime-semantic-parity`. Compare two runtime implementations for semantic equivalence.

## Saas Multitenancy Review

`saas-multitenancy-review`. Review SaaS multitenancy when tenant identity, pooled/siloed resources, quotas, storage, caches, jobs, search, exports, or operational isolation change, verifying cross-tenant safety and noisy-neighbor controls.

## Secret Environment Audit

`secret-environment-audit`. Audit secrets and environment configuration when credentials, API keys, signing secrets, database URLs, CI/CD variables, or public/private runtime configuration change.

## Semantic Compatibility Verification

`semantic-compatibility-verification`. Verify that a change preserves the meaning of a stable ATLAS contract.

## Seo Technical Audit

`seo-technical-audit`. Audit technical SEO when public web routes, domains, redirects, metadata, robots, sitemaps, canonicals, rendering, status codes, or crawl/index behavior change.

## Session Closeout

`session-closeout`. Capture completed work, validation, decisions, risks, pending work, and next actions at session end.

## Skill Quality Evaluation

`skill-quality-evaluation`. Measure registered ATLAS skills for structural completeness, discovery quality, trigger clarity, evidence strength, boundaries, and context discipline when the capability library changes or quality must be baselined.

## Skill Trigger Evaluation

`skill-trigger-evaluation`. Evaluate whether ATLAS skill discovery metadata and trigger conditions route representative requests to the intended capability without excessive collisions when skills are added, renamed, or overlap risk changes.

## Smoke Test Design

`smoke-test-design`. Create fast checks that verify critical framework and adapter behavior.

## Source Of Truth Validation

`source-of-truth-validation`. Verify that memory claims reference valid and authoritative project sources.

## Structured Data Validation

`structured-data-validation`. Validate JSON-LD and other structured data when public pages add or change schema markup, verifying syntax, page-content truthfulness, search eligibility, and non-conflicting canonical entities.

## Supply Chain Risk Audit

`supply-chain-risk-audit`. Audit dependency and build supply-chain risk when packages, lockfiles, registries, install scripts, CI actions, container bases, or third-party build inputs change.

## Support Classification

`support-classification`. Classify a runtime, capability, adapter, workflow, or feature by support level.

## Task Routing Policy

`task-routing-policy`. Map a request to roles, workflows, reviews, validation, and context requirements.

## Technical Debt Classification

`technical-debt-classification`. Classify and prioritize a technical debt item.

## Technical Roadmap Synthesis

`technical-roadmap-synthesis`. Create a sequenced technical roadmap from architecture, risk, product, platform, and operational inputs.

## Test Strategy Design

`test-strategy-design`. Create a proportionate testing strategy based on behavior, risk, and architecture.

## Threat Modeling

`threat-modeling`. Identify threats and controls for a system, feature, integration, or data flow.

## Transactional Email Delivery

`transactional-email-delivery`. Design transactional email for verification, recovery, invitations, receipts, and alerts with authoritative triggers, safe templates, idempotent retries, suppression, security, observability, and reconciliation.

## Universal Runtime Contract Design

`universal-runtime-contract-design`. Define runtime-neutral capabilities, envelopes, evidence, and conformance criteria.

## Version Migration Planning

`version-migration-planning`. Plan migration between ATLAS versions or compatible runtime adapter versions.

## Version Transition Validation

`version-transition-validation`. Verify that a patch is applied to the exact required base version.

## Visual Regression Review

`visual-regression-review`. Create and review deterministic browser screenshots when frontend changes need evidence against clipping, overflow, spacing, typography, crop, and layout regressions.

## Web Performance Field Readiness

`web-performance-field-readiness`. Assess user-facing performance before release when images, fonts, animation, WebGL, third-party scripts, or client JavaScript could threaten real-device experience.

## Webhook Reliability Review

`webhook-reliability-review`. Review inbound or outbound webhooks when event delivery, signatures, retries, ordering, deduplication, async processing, or replay behavior changes.

## Workstream Decomposition

`workstream-decomposition`. Divide a task into independently executable workstreams with explicit dependencies and completion criteria.
