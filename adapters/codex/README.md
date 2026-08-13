# ATLAS Codex Runtime

**Support:** Supported compatibility runtime  
**Canonical source:** Claude Code implementation and shared ATLAS framework

This adapter provides a functional Codex-oriented representation of ATLAS.
Its generated maps preserve semantic parity while Codex interprets canonical
workflows, skills, review gates, memory, and task protocol through runtime-native
or compatibility surfaces.

## Agent purpose labels

ATLAS does not maintain a second Codex-only label for an agent. The YAML
frontmatter `description` in `.claude/agents/<agent>.md` is the canonical
human-facing purpose label and routing summary.

This is intentional:

- Claude Code uses the canonical agent description for discovery/delegation.
- Codex plugin-compatible Markdown agents use the same `name` + `description`
  discovery model.
- Generated catalogs and future native adapter artifacts must preserve the same
  meaning rather than inventing a divergent label.

The canonical label contract is defined in `.claude/contracts/agent-contract.md`.
Capability grouping and principal skill affinities are defined in
`framework/capabilities/agent-taxonomy.yaml`.

## Skills

Canonical ATLAS skills live under `.claude/skills/`. Codex-native Agent Skills are
synchronized to `.agents/skills/` so Codex can discover project skills without
changing the canonical skill source.

Skill descriptions are routing contracts: they should explain both what a skill
does and when it should be activated. See `.claude/contracts/skill-contract.md`.

## Structure

- `agents/` compatibility role definitions
- `commands/` task entry points
- `skills/` reusable capability mappings
- `workflows/` execution procedures
- `reviews/` verification gates
- `runtime-manifest.json` support and mapping metadata
- `runtime-map.yaml` capability translation
- `catalogs/` generated human-readable capability catalogs
- `generated/*-map.json` machine-readable canonical-to-adapter maps

## Shared canonical assets

Codex uses the same:

- Framework models
- Contracts
- Memory and Obsidian capability views
- ADRs
- Documentation
- Templates
- Blueprints
- Compatibility policies

## Validation

Run:

```bash
python scripts/validate_capability_taxonomy.py
python scripts/validate_codex_adapter.py
python scripts/sync_codex_adapter.py --check
python scripts/sync_native_skills.py --check
python scripts/detect_runtime_drift.py
python scripts/run_codex_tests.py
```

## Limitations

Runtime tool invocation, installation surfaces, and picker presentation may differ
between Claude Code and Codex. These differences must not change semantic
responsibility, agent purpose, or validation expectations.
