# Skills

Skills contain reusable expertise that agents can invoke.

Every canonical skill lives at:

```text
.claude/skills/<skill-name>/SKILL.md
```

Browse every available skill and its routing description in the
[Skill Catalog](../../docs/skill-catalog.md).

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

Regenerate and validate the human-readable agent and skill catalogs with:

```bash
python scripts/generate_capability_catalogs.py
python scripts/generate_capability_catalogs.py --check
```
