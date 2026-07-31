# ATLAS Claude Code Bootstrap

@AGENTS.md

Claude Code is the canonical ATLAS runtime for this repository.

- At session start, read `VERSION`, `.atlas/continuity/resume-packet.json` when
  present, and the relevant documents under `.claude/memory/`.
- Use `.claude/commands/` as user-invoked entry points, native skills under
  `.claude/skills/*/SKILL.md`, and the closest canonical workflow, contracts,
  and review gates.
- Treat Markdown workflows and review gates as ATLAS procedures; native prompts
  and definitions still require runtime reasoning and do not execute by merely
  existing on disk.
- Inspect repository state before editing, preserve canonical knowledge across
  runtimes, and report validation and execution evidence before delivery.
