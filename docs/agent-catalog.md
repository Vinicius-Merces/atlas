# Agent Catalog

Canonical, generated inventory of every agent under `.claude/agents/`. Each entry mirrors its frontmatter `description`, which is the routing and discovery summary used by AI runtimes.

Regenerate both capability catalogs with `python scripts/generate_capability_catalogs.py`. Use `--check` in validation and CI.

Total: 88 agents.

## Adapter Drift Auditor

`adapter-drift-auditor`. Detects inventory, semantic, path, support, and documentation drift in runtime adapters.

## Adoption Architect

`adoption-architect`. Plans proportional ATLAS adoption for existing or new projects.

## AI Engineer

`ai-engineer`. Designs and implements AI features, model integrations, prompts, retrieval, tool use, and evaluation systems.

## Analytics Engineer

`analytics-engineer`. Designs trustworthy event schemas, metrics, transformations, dashboards, and product measurement systems.

## Audit Bundle Reviewer

`audit-bundle-reviewer`. Validates completeness and integrity of release or task audit bundles.

## Automation Engineer

`automation-engineer`. Designs reliable automation for validation, CI, release evidence, repository tasks, and governance checks.

## Backend Engineer

`backend-engineer`. Designs and implements reliable backend services, APIs, data flows, and integration logic.

## Beta Release Coordinator

`beta-release-coordinator`. Coordinates beta scope, compatibility, validation, migration guidance, known limitations, and release evidence.

## Change Provenance Engineer

`change-provenance-engineer`. Links changed files to tasks, decisions, validation, reviews, and runtimes.

## Checkpoint Integrity Reviewer

`checkpoint-integrity-reviewer`. Validates checkpoint completeness, consistency, and suitability for recovery or handoff.

## Cloud Architect

`cloud-architect`. Designs cloud architecture, service selection, network boundaries, resilience, cost, and migration strategy.

## Codex Runtime Engineer

`codex-runtime-engineer`. Builds and maintains the functional ATLAS runtime adapter for Codex.

## Compatibility Engineer

`compatibility-engineer`. Evaluates framework, runtime, project, artifact, and operational compatibility.

## Compliance Analyst

`compliance-analyst`. Maps system controls and evidence to applicable policies, contracts, and regulatory requirements.

## Conflict Resolution Engineer

`conflict-resolution-engineer`. Detects and resolves file, dependency, schema, contract, and knowledge conflicts.

## Content Designer

`content-designer`. Designs clear product language, interface copy, information hierarchy, and content patterns.

## Context Pack Engineer

`context-pack-engineer`. Builds bounded and source-linked context packs without duplicating project knowledge.

## Contract Test Engineer

`contract-test-engineer`. Designs and maintains tests that verify ATLAS contracts, registries, paths, and semantic compatibility.

## Data Engineer

`data-engineer`. Designs reliable data models, pipelines, migrations, transformations, and data quality controls.

## Dependency Manager

`dependency-manager`. Evaluates, upgrades, and governs third-party dependencies with compatibility, security, and maintenance awareness.

## Deprecation Manager

`deprecation-manager`. Governs deprecation, migration, replacement readiness, communication, and removal.

## Design System Engineer

`design-system-engineer`. Builds and governs reusable design tokens, components, patterns, documentation, and migration paths.

## Developer Experience Engineer

`developer-experience-engineer`. Improves setup, tooling, documentation, local workflows, feedback speed, and maintainability for developers.

## DevOps Engineer

`devops-engineer`. Designs and maintains deployment, infrastructure, environments, automation, and operational safety.

## Documentation Architect

`documentation-architect`. Designs documentation structure, navigation, canonical ownership, cross-links, and lifecycle.

## Documentation Engineer

`documentation-engineer`. Maintains clear, accurate, navigable documentation for users, developers, architecture, and operations.

## Enterprise Architect

`enterprise-architect`. Aligns system portfolios, business capabilities, platforms, data domains, integrations, and technical strategy.

## Evidence Ledger Architect

`evidence-ledger-architect`. Defines task evidence, attribution, integrity, and retention requirements.

## Execution Continuity Engineer

`execution-continuity-engineer`. Designs resumable execution state, checkpoints, and continuation plans.

## Experimentation Analyst

`experimentation-analyst`. Designs experiments, hypotheses, metrics, segmentation, analysis, and decision rules.

## FinOps Engineer

`finops-engineer`. Analyzes cloud and platform cost, unit economics, allocation, waste, commitments, and optimization trade-offs.

## Frontend Engineer

`frontend-engineer`. Implements maintainable, accessible, performant web interfaces while preserving existing behavior and design systems.

## Generative Engine Optimization Strategist

`generative-engine-optimization-strategist`. Leads evidence-based GEO strategy for AI-search visibility, entity authority, answer-ready content, and measurement without speculative ranking claims.

## Governance Steward

`governance-steward`. Maintains standards, controls, exceptions, decision rights, evidence requirements, and governance health.

## Integration Engineer

`integration-engineer`. Designs and implements reliable contracts between internal and external systems.

## Knowledge Contradiction Reviewer

`knowledge-contradiction-reviewer`. Reviews incompatible project claims and blocks silent resolution of disputed facts.

## Knowledge Engineer

`knowledge-engineer`. Structures project knowledge, memory, links, ownership, provenance, and retrieval readiness.

## Localization Engineer

`localization-engineer`. Prepares products for translation, locale behavior, cultural adaptation, and international formatting.

## Manual Deployment Auditor

`manual-deployment-auditor`. Reviews manually applied incremental patches and their deployment receipts.

## Manual Deployment Safety Engineer

`manual-deployment-safety-engineer`. Designs safe, explicit, and verifiable manual patch application.

## Memory Governance Architect

`memory-governance-architect`. Defines ownership, sources, freshness, contradiction, and retirement rules for portable project memory.

## Merge Readiness Reviewer

`merge-readiness-reviewer`. Verifies that parallel workstreams can be reconciled and merged safely.

## Migration Architect

`migration-architect`. Designs safe migrations between framework versions, architectures, platforms, data models, and runtimes.

## Mobile Engineer

`mobile-engineer`. Designs and implements reliable, accessible, performant mobile applications and platform integrations.

## Monorepo Maintainer

`monorepo-maintainer`. Governs package boundaries, shared tooling, dependency direction, affected builds, and safe cross-package changes.

## Orchestrator

`orchestrator`. Coordinates complex tasks, selects specialist agents, enforces contracts, and owns delivery sequencing.

## Parallel Execution Architect

`parallel-execution-architect`. Designs safe parallel execution graphs across supported ATLAS runtimes.

## Patch Integrity Engineer

`patch-integrity-engineer`. Builds and verifies incremental framework patches against an explicit base version.

## Performance Engineer

`performance-engineer`. Measures, diagnoses, and improves application performance using explicit budgets and evidence.

## Platform Engineer

`platform-engineer`. Builds reusable internal platforms, golden paths, shared tooling, and safe self-service foundations.

## Policy Enforcement Architect

`policy-enforcement-architect`. Defines machine-readable ATLAS policies and enforcement outcomes.

## Policy Engineer

`policy-engineer`. Converts stable governance requirements into testable policy-as-code rules and exception paths.

## Policy Exception Reviewer

`policy-exception-reviewer`. Reviews scoped deviations, expiration, compensating controls, and residual risk.

## Privacy Engineer

`privacy-engineer`. Reviews data collection, purpose, retention, sharing, user rights, and privacy risk.

## Product Architect

`product-architect`. Defines product structure, system boundaries, requirements, and architecture trade-offs before implementation.

## Product Manager

`product-manager`. Frames product problems, outcomes, priorities, requirements, metrics, and delivery scope.

## Project Health Analyst

`project-health-analyst`. Assesses project health across product, architecture, delivery, operations, trust, knowledge, and economics.

## Project Memory Curator

`project-memory-curator`. Maintains portable project memory, summaries, decisions, ownership, and freshness.

## Project State Reconciler

`project-state-reconciler`. Compares memory, ADRs, continuity artifacts, and repository evidence to propose safe updates.

## QA Engineer

`qa-engineer`. Validates acceptance criteria, regressions, edge cases, and release readiness independently from implementation.

## Reference Implementation Reviewer

`reference-implementation-reviewer`. Reviews examples and starter projects for architectural quality, completeness, and instructional value.

## Release Integrity Engineer

`release-integrity-engineer`. Verifies version consistency, manifests, checksums, package completeness, provenance, and release artifact integrity.

## Release Manager

`release-manager`. Coordinates release scope, versioning, evidence, approvals, communications, and rollout readiness.

## Reliability Engineer

`reliability-engineer`. Defines service reliability, observability, incident readiness, recovery, and operational risk controls.

## Resume Packet Reviewer

`resume-packet-reviewer`. Validates whether a repository contains enough current evidence to resume work safely.

## Runtime Adapter Engineer

`runtime-adapter-engineer`. Translates canonical ATLAS definitions into runtime-specific formats without changing semantic intent.

## Runtime Capability Mapper

`runtime-capability-mapper`. Maps canonical ATLAS capabilities to runtime-specific tools, structures, and invocation methods.

## Runtime Catalog Maintainer

`runtime-catalog-maintainer`. Maintains generated and human-readable catalogs of runtime capabilities.

## Runtime Conformance Auditor

`runtime-conformance-auditor`. Audits supported runtimes against the universal ATLAS runtime contract.

## Runtime Execution Planner

`runtime-execution-planner`. Turns a routed task and context pack into a runtime-neutral execution plan.

## Runtime Handoff Coordinator

`runtime-handoff-coordinator`. Coordinates safe transfer of active tasks between Claude Code, Codex, and future supported runtimes.

## Runtime Parity Reviewer

`runtime-parity-reviewer`. Reviews semantic, capability, governance, knowledge, and validation parity between supported runtimes.

## Runtime Synchronization Engineer

`runtime-synchronization-engineer`. Synchronizes runtime adapters with canonical ATLAS registry collections and contracts.

## Search Retrieval Engineer

`search-retrieval-engineer`. Designs search, indexing, retrieval, ranking, chunking, embeddings, and RAG systems.

## Security Engineer

`security-engineer`. Reviews trust boundaries, authentication, authorization, secrets, dependencies, and abuse risks.

## Session Continuity Engineer

`session-continuity-engineer`. Creates session bootstrap, closeout, and recovery artifacts across supported runtimes.

## Solution Blueprint Engineer

`solution-blueprint-engineer`. Selects and adapts reusable project blueprints to product and technical context.

## Stability Engineer

`stability-engineer`. Protects stable contracts, canonical paths, compatibility expectations, and beta release integrity.

## Support Policy Maintainer

`support-policy-maintainer`. Maintains support states, runtime commitments, known limitations, and support lifecycle transitions.

## Task Routing Engineer

`task-routing-engineer`. Designs explainable routing across roles, skills, workflows, reviews, and validation.

## Technical Auditor

`technical-auditor`. Performs evidence-based audits of architecture, code, operations, security, delivery, and documentation.

## Technical Debt Steward

`technical-debt-steward`. Identifies, classifies, prioritizes, and tracks technical debt across systems and teams.

## Technical Program Manager

`technical-program-manager`. Coordinates complex multi-team technical programs, milestones, dependencies, risks, decisions, and delivery evidence.

## Test Automation Engineer

`test-automation-engineer`. Designs maintainable automated testing systems across unit, integration, end-to-end, and non-functional layers.

## Threat Modeling Engineer

`threat-modeling-engineer`. Models assets, trust boundaries, threat actors, abuse paths, controls, and residual security risk.

## Universal Runtime Architect

`universal-runtime-architect`. Defines provider-neutral ATLAS runtime requirements and compatibility boundaries.

## UX Director

`ux-director`. Reviews and directs interaction design, accessibility, content hierarchy, and user experience quality.

## Workstream Coordinator

`workstream-coordinator`. Creates, assigns, tracks, and closes independent workstreams.
