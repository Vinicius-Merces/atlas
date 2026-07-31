# Skills

Skills contain reusable expertise that agents can invoke.

Every canonical skill lives at:

```text
.claude/skills/<skill-name>/SKILL.md
```

This is the native Claude Code skill layout. Codex-native repository wrappers
under `.agents/skills/` are generated from these canonical files and must not
redefine their meaning.

A skill should be focused, bounded, testable, and independent of one specific
project unless clearly marked as project-specific. Each skill must follow
`.claude/contracts/skill-contract.md`.

Validate both runtime surfaces with:

```bash
python scripts/sync_native_skills.py --check
```
