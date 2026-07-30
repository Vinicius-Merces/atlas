# ATLAS AI Engineering Framework

**Version:** `0.1.0-beta.10`  
**Status:** Beta / Provenance, Evidence Ledger and Auditability

ATLAS coordinates software engineering through shared memory, specialized
agents, workflows, review gates, runtime contracts, resumable tasks, portable
continuity, conflict-safe execution, and auditable evidence.

## Beta.10 milestone

Every meaningful task can now leave a traceable evidence chain from request to
manual deployment.

### New capabilities

- Task evidence ledger
- Change provenance
- Decision-to-code traceability
- Validation evidence records
- Manual deployment receipts
- Runtime attribution
- Audit bundle generation
- Evidence integrity verification

## Evidence chain

```text
Request
  ↓
Task envelope
  ↓
Context and decisions
  ↓
Execution plan
  ↓
Changed files
  ↓
Validation and reviews
  ↓
Checkpoint or result
  ↓
Manual deployment receipt
  ↓
Audit bundle
```

## Commands

```bash
python scripts/create_evidence_record.py --task-id task-001 --runtime codex
python scripts/record_manual_deploy.py --from-version 0.1.0-beta.9 --to-version 0.1.0-beta.10
python scripts/build_audit_bundle.py
python scripts/verify_evidence_integrity.py
```

All updates remain compatible with manual extraction and file-by-file
deployment.
