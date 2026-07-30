# ATLAS AI Engineering Framework

**Version:** `0.1.0-beta.8`  
**Status:** Beta / Portable Project Memory and Session Continuity

ATLAS coordinates software engineering through shared memory, specialized
agents, workflows, review gates, runtime contracts, resumable tasks, parallel
workstreams, and portable project continuity.

## Beta.8 milestone

Project context can now travel with the repository instead of depending on one
chat session or one model.

### New capabilities

- Portable project brief
- Session bootstrap
- Session closeout
- Resume packet generation
- Memory freshness checks
- Decision and progress snapshots
- Codex and Claude startup instructions
- Cross-session continuity validation
- Repository-native project context

## Portable memory flow

```text
Project work
  ↓
Memory and decision updates
  ↓
Session closeout
  ↓
Portable resume packet
  ↓
Repository clone
  ↓
Codex or Claude Code bootstrap
  ↓
Continue from current project state
```

## Commands

```bash
python scripts/build_project_brief.py
python scripts/create_session_brief.py --summary "Current project state"
python scripts/validate_memory_freshness.py
python scripts/build_resume_packet.py
```

The repository remains the durable project brain. Runtime chat history is
helpful, but never the sole source of truth.
