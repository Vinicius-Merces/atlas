---
name: data-import-export-workflow
description: "Design bulk data import and export workflows for CSV, spreadsheet, archive, or generated datasets, covering authorization, schema mapping, preview, validation, partial errors, idempotency, background processing, progress, large files, privacy, reconciliation, and downloadable artifact lifecycle."
---

# Data Import & Export Workflow

## Purpose

Design bulk movement of business data as a resumable, auditable workflow rather than a synchronous file loop that fails halfway without clear state.

## Trigger conditions

Use for CSV/XLSX imports, catalog/contact/property migrations, bulk updates, data exports, report archives, account portability, or large downloadable datasets.

## Inputs

- Source/target schema and mapping rules
- File formats, sizes, row counts, and encoding expectations
- Actor/tenant authorization and privacy rules
- Error tolerance and atomicity expectations
- Background processing/storage constraints

## Procedure

1. Define import/export job ownership, tenant scope, lifecycle states, and authoritative result.
2. Validate format, size, encoding, headers/schema, and high-level structure before expensive processing.
3. Provide mapping/preview for user-controlled schemas when ambiguity is expected.
4. Define row-level validation, duplicate identity, upsert/insert policy, reference resolution, and partial-error semantics.
5. Make retries safe through job idempotency, checkpoints, deduplication, or immutable source artifacts.
6. Move long-running work to reliable background execution with progress and cancellation semantics.
7. Bound memory and row/result sizes; stream/chunk where appropriate rather than loading arbitrary files entirely.
8. Produce an error/report artifact that helps users repair invalid rows without leaking data across tenants.
9. Protect exports with authorization at generation and download, scoped artifact access, expiration, retention, and deletion.
10. Reconcile job metadata, database mutations, and output objects after interruptions.

## Outputs

- Import/export job and state model
- Mapping/validation/error policy
- Idempotency/chunking/background design
- Artifact authorization/lifecycle model
- Reconciliation and negative-path evidence

## Dependencies

- `file-upload-storage-design` for source/output artifacts
- `background-job-reliability` for long-running jobs
- `authorization-boundary-review` and `saas-multitenancy-review`
- `database-schema-review` for mapped target invariants

## Limitations

Spreadsheet parsing libraries and file-format edge cases remain implementation-specific. Bulk operations may require domain-specific transaction boundaries rather than all-or-nothing semantics.

## Validation

- Test empty, malformed, oversized, duplicate, partially invalid, unauthorized, interrupted, retried, cancelled, and large representative jobs.
- Verify exported data scope and artifact expiration/deletion.
- Reconcile persisted job state against actual imported/exported records.
