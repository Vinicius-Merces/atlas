# Hook Contract

Status: experimental. Not yet part of the stable `core-contracts.json`
baseline; enforced by dedicated tests under `tests/hooks/`, not by
`scripts/validate_contracts.py`.

A hook is a mechanical enforcement or reminder bound to a Claude Code
lifecycle event. Hooks exist to make an already-stated rule happen
automatically instead of depending on an agent remembering it.

## Required properties

Every hook entry in `.claude/hooks/hooks.json` must declare:

- Event: one of the real Claude Code hook events (for example `PreToolUse`,
  `PostToolUse`, `SessionStart`, `SessionEnd`, `PreCompact`, `Stop`).
- Matcher: a plain tool-name string or alternation (`Write`, `Write|Edit`) or
  a regex. Never a boolean expression language; that syntax does not exist in
  Claude Code and will silently never match.
- A `description` explaining what it does and why.
- Behavior class: **blocking** (exits 2, or JSON `permissionDecision: "deny"`
  on `PreToolUse`) or **advisory** (exits 0 always, never affects control
  flow). This must be stated explicitly in the hook's own script docstring.
- A script under `.claude/hooks/scripts/`, referenced as
  `"command": "python", "args": ["${CLAUDE_PLUGIN_ROOT}/hooks/scripts/<name>.py"]`,
  covered by a test in `tests/hooks/`.

  Scripts must live inside `.claude/` (not a sibling top-level directory such
  as `scripts/`). When ATLAS is installed as a Claude Code plugin, only the
  declared plugin `source` (`.claude/`) is copied into the plugin cache — a
  script outside it would exist in this repository but not in any project
  that installs ATLAS as a plugin.

  Known limitation: `${CLAUDE_PLUGIN_ROOT}` is confirmed to resolve correctly
  when ATLAS is installed as a plugin. Whether it also resolves when this
  repository's own `.claude/hooks/hooks.json` is loaded directly (not via a
  plugin install) is not clearly documented upstream. `${CLAUDE_PROJECT_DIR}`
  is documented as always available, but cannot alone locate a plugin's
  cached files from a different project, so it cannot replace
  `${CLAUDE_PLUGIN_ROOT}` for this use case. Treat direct-repository hook
  execution as unverified until confirmed in a real session.

## Design rules

- A blocking hook must be justified by a rule that already exists elsewhere
  in ATLAS (CLAUDE.md, AGENTS.md, `.claude/rules/global.md`, or a canonical
  contract). Hooks encode existing rules mechanically; they do not introduce
  new policy on their own.
- A blocking hook must not assume a target project's stack (do not hardcode
  npm/pnpm/yarn, TypeScript, or any single toolchain) unless the hook is
  explicitly scoped and documented as stack-specific and opt-in.
- An advisory hook must never use an exit code or JSON shape that can block
  or force continuation (no exit 2 on `Stop`/`SessionEnd`).
- Every hook script must fail open on its own internal errors: catch
  unexpected exceptions and exit 0 rather than crash the parent tool call or
  session.
- `.claude/hooks/hooks.json` is loaded automatically by any project that
  installs ATLAS as a Claude Code plugin (see `.claude-plugin/marketplace.json`).
  A new blocking hook changes behavior for every such installation, not just
  this repository, and must be evaluated with that blast radius in mind.
