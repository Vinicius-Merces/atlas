# Skill Catalog

Canonical, generated inventory of every skill under `.claude/skills/<skill-name>/SKILL.md`. Each entry mirrors its frontmatter `description`, which is the routing and discovery summary used by AI runtimes.

Regenerate both capability catalogs with `python scripts/generate_capability_catalogs.py`. Use `--check` in validation and CI.

Total: 96 skills.

## Accessibility Audit

`accessibility-audit`. Review user-facing work for common accessibility failures.

## Adapter Drift Detection

`adapter-drift-detection`. Detect divergence between a supported runtime adapter and canonical ATLAS.

## ADR Authoring

`adr-authoring`. Capture an important architecture decision with sufficient context and traceability.

## AI System Design

`ai-system-design`. Design an AI-enabled system with explicit capabilities, limitations, data flow, and evaluation.

## API Contract Analysis

`api-contract-analysis`. Assess API compatibility and identify migration risks.

## Architecture Assessment

`architecture-assessment`. Evaluate whether a proposed change fits existing architecture and preserves clear boundaries.

## Architecture Audit

`architecture-audit`. Audit architecture for clarity, ownership, coupling, resilience, and alignment.

## Architecture Portfolio Assessment

`architecture-portfolio-assessment`. Assess multiple systems as a portfolio rather than isolated architectures.

## Audit Bundle Assembly

`audit-bundle-assembly`. Assemble a navigable manifest of evidence for a task, release, or deployment.

## Blueprint Selection

`blueprint-selection`. Choose the closest ATLAS blueprint for a project.

## Change Provenance Mapping

`change-provenance-mapping`. Map file changes to tasks, decisions, runtimes, validation, and reviews.

## Cloud Cost Analysis

`cloud-cost-analysis`. Analyze cloud or platform spending and identify evidence-based optimization opportunities.

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

## Core Contract Stabilization

`core-contract-stabilization`. Evaluate whether a contract is stable enough for a beta support commitment.

## Database Migration Analysis

`database-migration-analysis`. Assess schema and data migrations for integrity, compatibility, and operational risk.

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

## Event Taxonomy Design

`event-taxonomy-design`. Design stable, privacy-aware analytics events and properties.

## Evidence Record Design

`evidence-record-design`. Create a portable evidence record for a task or workstream.

## Execution Checkpointing

`execution-checkpointing`. Capture immutable execution state at a meaningful task boundary.

## Experiment Design

`experiment-design`. Design an experiment with explicit hypothesis, metrics, population, analysis, and decision rules.

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

## Observability Design

`observability-design`. Design logs, metrics, traces, dashboards, and alerts for a feature or service.

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

## Semantic Compatibility Verification

`semantic-compatibility-verification`. Verify that a change preserves the meaning of a stable ATLAS contract.

## Session Closeout

`session-closeout`. Capture completed work, validation, decisions, risks, pending work, and next actions at session end.

## Smoke Test Design

`smoke-test-design`. Create fast checks that verify critical framework and adapter behavior.

## Source Of Truth Validation

`source-of-truth-validation`. Verify that memory claims reference valid and authoritative project sources.

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

## Workstream Decomposition

`workstream-decomposition`. Divide a task into independently executable workstreams with explicit dependencies and completion criteria.
