# Changelog

## 0.1.0

### Added

- Stable release manifest, migration, validation, exercise evidence, and
  reproducible distribution artifacts
- Direct beta.11-to-stable incremental upgrade path

### Changed

- Version channel promoted from `0.1.0-rc.1` to stable `0.1.0`
- Claude Code and Codex support graduated from beta-supported to supported
- Core contract classification promoted from `stable-rc` to `stable`
- Stable support, compatibility, deprecation, rollback, and known-limitations
  commitments activated

### Validation

- Tagged RC source passed two GitHub-hosted validation runs
- Post-RC hygiene exercise completed without blockers on the corrected source
- Full local validation, deterministic package reproduction, beta.11 upgrade,
  clean installation, recovery, and audit-integrity gates are required by the
  stable checklist

## 0.1.0-rc.1

### Added

- Release-candidate manifests, migration guidance, validation evidence, and
  reproducible distribution artifacts
- Explicit `rc` contract-stability classification

### Changed

- Version channel promoted from `0.1.0-beta.12` to `0.1.0-rc.1`
- Core contract status promoted from `stable-beta` to `stable-rc`
- The support matrix now documents beta-to-RC and RC-to-stable transitions
- Release metadata now identifies the `rc` channel

### Fixed

- Removed user-local `.vscode/extensions.json` from version control while
  preserving it outside release payloads
- Corrected stale known-limitations text that classified Codex as experimental
- Normalized release-document EOF formatting

### Promotion evidence

- GitHub pull request #1 merged as
  `6f8d82dc3241a923ea0ee0f81e1e02e50b45c521`
- GitHub-hosted CI and independent review were reported as passed before merge
- The merge contains the finalized beta.12 source at
  `5fa430968011216c265c05add647ff14cf1858d0`

## 0.1.0-beta.12

### Added

- Deterministic cumulative, incremental, and recovery release builders
- Package integrity manifests, checksums, validators, and install simulators
- Centralized version-source management with historical-artifact protection
- Schema validation with positive fixtures for every registered schema
- Generated Codex maps for agents, commands, skills, workflows, and reviews
- Runtime lifecycle end-to-end coverage, including continuity, conflicts,
  reconciliation, evidence, deployment receipts, and audit integrity
- Executable release, runtime, schema, CI, support, source-of-truth, package,
  deletion, and repository-cleanliness policies
- Durable architecture, business, operations, and contradiction memories
- Memory freshness, knowledge-link, documentation, and exception validators
- Release candidate and stable release checklists
- Complete installation, runtime, deployment, release, and troubleshooting
  documentation

### Changed

- Canonical agent definitions now live exclusively under `.claude/agents/`
- Codex is beta-supported with generated, resolvable parity maps
- CI installs explicit test dependencies and exercises all release gates
- Manual incremental packages expose `.claude/` payload through
  `CLAUDE-DIRECTORY/` and require exact declared operations
- Package source selection excludes local state, editor settings, reports,
  caches, secrets, and generated distribution artifacts

### Fixed

- Source-of-truth, Codex synchronization, runtime drift, support-policy, task
  routing, and registry inconsistencies
- Fragile policy validation and unsafe or implicit manual deletion behavior
- Non-deterministic release archives and incomplete artifact integrity checks

### Validation

- All repository validators, policy evaluators, schema checks, and automated
  tests pass locally
- Clean install, beta.11 incremental upgrade, recovery, deterministic rebuild,
  checksum tamper, and audit tamper simulations pass locally

### Known limitations

- GitHub-hosted CI must still execute on the published branch
- Independent release review and approval are still required before RC
- RC and stable promotion are intentionally not authorized by this release

## 0.1.0-beta.11

### Added

- Policy Enforcement Architect agent
- Manual Deployment Safety Engineer agent
- Policy Exception Reviewer agent
- Policy rule design skill
- Manual deployment preflight skill
- Version transition validation skill
- Policy exception handling skill
- Policy evaluation workflow
- Manual deployment preflight workflow
- Policy exception workflow
- Policy compliance review gate
- Manual deployment safety review gate
- Policy exception review gate
- `/atlas-policy-check`, `/atlas-deploy-preflight`, and `/atlas-policy-exception`
- Policy rule schema
- Policy evaluation report schema
- Policy exception schema
- Deployment preflight report schema
- Policy evaluator
- Manual deployment preflight tool
- Version transition validator
- Policy report builder
- Policy conformance tests
- Policy enforcement model
- Manual deployment safety model
- Policy exception model
- Version transition model
- Visible `CLAUDE-DIRECTORY` package mapping

### Changed

- Version promoted to `0.1.0-beta.11`
- Incremental packages now expose `.claude` updates through `CLAUDE-DIRECTORY`
- Universal runtime contract includes policy evaluation capabilities
- Claude Code and Codex declarations include deployment preflight support

## 0.1.0-beta.10

### Added

- Evidence Ledger Architect agent
- Change Provenance Engineer agent
- Audit Bundle Reviewer agent
- Manual Deployment Auditor agent
- Evidence record design skill
- Change provenance mapping skill
- Audit bundle assembly skill
- Manual deployment receipt skill
- Evidence capture workflow
- Provenance reconciliation workflow
- Audit bundle workflow
- Manual deployment audit workflow
- Evidence integrity review gate
- Provenance review gate
- Manual deployment review gate
- `/atlas-evidence`, `/atlas-provenance`, `/atlas-audit-bundle`, and `/atlas-deploy-receipt`
- Evidence record schema
- Change provenance schema
- Manual deployment receipt schema
- Audit bundle manifest schema
- Evidence record creator
- Manual deployment receipt creator
- Audit bundle builder
- Evidence integrity verifier
- Provenance conformance tests
- Evidence ledger model
- Change provenance model
- Manual deployment receipt model
- Audit bundle model
- Auditability and manual deployment guides

### Changed

- Version promoted to `0.1.0-beta.10`
- Universal runtime contract now requires evidence and provenance capabilities
- Claude Code and Codex declarations include auditability support
- Incremental package instructions include manual deployment receipt guidance

## 0.1.0-beta.9

### Added

- Memory Governance Architect agent
- Project State Reconciler agent
- Knowledge Contradiction Reviewer agent
- Memory drift analysis skill
- Source-of-truth validation skill
- Continuity reconciliation skill
- Memory update proposal skill
- Memory drift audit workflow
- Project-state reconciliation workflow
- Continuity refresh workflow
- Memory governance review gate
- Contradiction review gate
- Source-of-truth review gate
- `/atlas-memory-drift`, `/atlas-reconcile-memory`, and `/atlas-refresh-continuity`
- Memory drift report schema
- Contradiction register schema
- Reconciliation proposal schema
- Source-of-truth manifest schema
- Memory drift auditor
- Source-of-truth validator
- Reconciliation proposal builder
- Continuity refresh tool
- Memory governance conformance tests
- Memory governance model
- Project-state reconciliation model
- Contradiction management model
- Source-of-truth model
- Manual continuity refresh guide

### Changed

- Version promoted to `0.1.0-beta.9`
- Portable memory now includes drift and contradiction governance
- Claude Code and Codex declarations include project-state reconciliation capabilities
- Incremental package instructions explicitly prioritize manual deployment

## 0.1.0-beta.8

### Added

- Project Memory Curator agent
- Session Continuity Engineer agent
- Resume Packet Reviewer agent
- Project brief synthesis skill
- Session closeout skill
- Memory freshness audit skill
- Resume packet assembly skill
- Session bootstrap workflow
- Session closeout workflow
- Cross-session recovery workflow
- Project memory review gate
- Session continuity review gate
- Resume packet review gate
- `/atlas-brief`, `/atlas-close-session`, `/atlas-resume-packet`, and `/atlas-memory-freshness`
- Project brief schema
- Session brief schema
- Resume packet schema
- Project brief builder
- Session brief creator
- Memory freshness validator
- Resume packet builder
- Portable memory tests
- Project continuity model
- Session brief model
- Memory freshness model
- Resume packet model
- VS Code Codex bootstrap guide
- Claude Code bootstrap guide
- Cross-session continuity guide

### Changed

- Version promoted to `0.1.0-beta.8`
- Universal runtime contract now includes portable project-memory capabilities
- Claude Code and Codex declarations now include session bootstrap and resume support
- Incremental delivery remains the default package format

## 0.1.0-beta.7

### Added

- Parallel Execution Architect agent
- Workstream Coordinator agent
- Conflict Resolution Engineer agent
- Merge Readiness Reviewer agent
- Workstream decomposition skill
- Resource claim design skill
- Conflict prediction skill
- Result reconciliation skill
- Parallel execution workflow
- Workstream merge workflow
- Shared-state protection workflow
- Parallel execution review gate
- Resource claim review gate
- Merge readiness review gate
- `/atlas-parallelize`, `/atlas-claim`, `/atlas-merge-ready`, and `/atlas-reconcile`
- Workstream schema
- Resource claim schema
- Parallel execution manifest schema
- Reconciliation report schema
- Workstream generator
- Resource claim tool
- Conflict detector
- Merge readiness validator
- Reconciliation report builder
- Parallel execution conformance tests
- Parallel execution model
- Resource claim model
- Conflict model
- Result reconciliation model
- Parallel execution and merge guides

### Changed

- Version promoted to `0.1.0-beta.7`
- Universal runtime contract now includes workstream and conflict-safe execution capabilities
- Claude Code and Codex runtime declarations include parallel execution support
- Incremental delivery remains the default package format

## 0.1.0-beta.6

### Added

- Runtime Handoff Coordinator agent
- Execution Continuity Engineer agent
- Checkpoint Integrity Reviewer agent
- Runtime handoff design skill
- Execution checkpoint skill
- Continuation planning skill
- Runtime handoff workflow
- Interrupted-task recovery workflow
- Continuation planning workflow
- Handoff review gate
- Checkpoint integrity review gate
- `/atlas-checkpoint`, `/atlas-handoff`, and `/atlas-resume`
- Checkpoint schema
- Handoff manifest schema
- Continuation plan schema
- Checkpoint creation script
- Handoff creation script
- Handoff validator
- Continuation-plan builder
- Cross-runtime handoff tests
- Runtime handoff model
- Execution continuity model
- Checkpoint model
- Handoff and recovery guides

### Changed

- Version promoted to `0.1.0-beta.6`
- Universal runtime contract now requires checkpoint and handoff support
- Claude Code and Codex declarations now include resumable execution capabilities
- Incremental delivery remains the default package format

## 0.1.0-beta.5

### Added

- Executable task router
- Context pack generator
- Task envelope validator
- Execution result validator
- Runtime execution planner
- Patch preflight validator
- Task routing examples
- Runtime execution plan schema
- Context pack manifest schema
- Runtime execution workflow
- Task envelope lifecycle workflow
- Context assembly review gate
- Execution planning review gate
- `/atlas-execute-plan` and `/atlas-patch-check`
- Incremental package specification
- Patch application guide
- Runtime execution guide
- Task envelope lifecycle model
- Context resolution model
- Incremental delivery model

### Changed

- Version promoted to `0.1.0-beta.5`
- Universal runtime contract now references executable routing and context tools
- Claude Code and Codex declarations include task-routing and context-pack capabilities
- Release packaging now supports verifiable incremental patches

## 0.1.0-beta.4

### Added

- Universal Runtime Architect agent
- Task Routing Engineer agent
- Context Pack Engineer agent
- Runtime Conformance Auditor agent
- Universal runtime contract, task routing, context pack, and conformance skills
- Task routing, context pack, and runtime conformance workflows
- Universal runtime, routing, context, and conformance review gates
- `/atlas-route`, `/atlas-context-pack`, and `/atlas-conformance`
- Provider-neutral runtime contract
- Claude Code and Codex runtime declarations
- Task envelope and execution-result schemas
- Runtime conformance scripts and tests
- Universal runtime, task routing, context pack, and conformance models

### Changed

- Version promoted to `0.1.0-beta.4`
- Claude Code and Codex now declare support against one universal contract

All notable changes to ATLAS are documented here.

## 0.1.0-beta.3

### Added

- Runtime Synchronization Engineer agent
- Runtime Catalog Maintainer agent
- Adapter Drift Auditor agent
- Registry-to-runtime generation skill
- Adapter drift detection skill
- Command catalog synthesis skill
- Runtime synchronization workflow
- Adapter drift audit workflow
- Runtime catalog publication workflow
- Runtime synchronization review gate
- Adapter drift review gate
- `/atlas-runtime-sync`, `/atlas-runtime-drift`, and `/atlas-runtime-catalog`
- Root `AGENTS.md`
- Codex task protocol
- Shared execution evidence specification
- Generated Codex agent catalog
- Generated Codex command catalog
- Generated Codex skill catalog
- Generated Codex workflow catalog
- Generated Codex review catalog
- Codex runtime synchronization script
- Runtime drift detection script
- Codex catalog tests
- Full registry parity tests
- Runtime synchronization report template
- Adapter drift report template
- Runtime synchronization model
- Adapter drift model
- Execution evidence model

### Changed

- Codex adapter now derives complete catalogs from the canonical registry
- Codex support status updated to synchronized beta runtime
- Release validation expanded with drift detection
- Version promoted to `0.1.0-beta.3`

## 0.1.0-beta.2

### Added

- Beta support for Claude Code and Codex
- Functional Codex adapter
- Runtime parity tests
- Dual-runtime workflows

## 0.1.0-beta.1

### Added

- First public beta
- Stable core contracts
