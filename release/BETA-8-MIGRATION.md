# Migration to 0.1.0-beta.8

Apply this patch only over `0.1.0-beta.7`.

After application:

```bash
python scripts/build_project_brief.py
python scripts/create_session_brief.py --summary "Initial continuity snapshot"
python scripts/validate_memory_freshness.py
python scripts/build_resume_packet.py
```

Commit `.atlas/continuity/` when it contains project-safe context needed by the
next runtime or session.
