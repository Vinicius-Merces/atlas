# Changelog

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
