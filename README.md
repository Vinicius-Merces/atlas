# ATLAS AI Engineering Framework

**Version:** `0.1.0-beta.9`  
**Status:** Beta / Memory Governance and Project-State Reconciliation

ATLAS coordinates software engineering through shared memory, specialized
agents, workflows, review gates, runtime contracts, resumable tasks, portable
continuity, and conflict-safe execution.

## Beta.9 milestone

Project memory can now be compared against repository evidence to detect stale,
contradictory, duplicated, or orphaned knowledge before Claude Code or Codex
continues work.

### New capabilities

- Memory drift detection
- Project-state reconciliation
- Contradiction register
- Source-of-truth validation
- Orphaned decision detection
- Memory update proposals
- Safe continuity refresh
- Manual-deploy friendly patch instructions

## Reconciliation flow

```text
Repository state
  + Memory
  + ADRs
  + Session briefs
  + Resume packet
        ↓
Memory drift analysis
        ↓
Contradiction and staleness report
        ↓
Reconciliation proposal
        ↓
Human or governed approval
        ↓
Updated portable project context
```

## Commands

```bash
python scripts/audit_memory_drift.py
python scripts/build_reconciliation_proposal.py
python scripts/validate_source_of_truth.py
python scripts/refresh_continuity_artifacts.py
```

All patch files remain directly copyable for manual deployment. Validation
scripts are optional post-deploy checks.
