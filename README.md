# ATLAS AI Engineering Framework

**Version:** `0.1.1`
**Status:** Stable

ATLAS is a repository-native engineering operating framework for teams that
use AI coding runtimes. It keeps durable project knowledge, contracts,
specialist responsibilities, workflows, review gates, continuity artifacts,
policies, and release evidence together so work can continue without depending
on chat history.

## Who it is for

ATLAS is intended for engineers and teams that need AI-assisted work to remain
consistent, reviewable, portable across sessions, and compatible with more than
one runtime. It is especially useful when architecture, business constraints,
manual deployment, auditability, or cross-session handoff matter.

## What it solves

- Preserves validated knowledge in the repository.
- Separates durable memory from temporary execution state.
- Protects meaning through contracts, policies, tests, and review gates.
- Routes tasks through reusable agents, skills, workflows, and commands.
- Shares canonical knowledge between Claude Code and Codex.
- Produces checkpoints, handoffs, resume packets, evidence, and audit bundles.
- Builds reproducible cumulative, incremental, and recovery packages.
- Supports manual updates with explicit additions, replacements, and deletions.

## Architecture

```text
Knowledge     .claude/memory, docs, framework, ADRs
Capabilities .claude/skills, schemas, templates, adapters
Execution    .claude/agents, workflows, commands, task artifacts
Governance   contracts, reviews, policies, tests, evidence
```

Claude Code is the canonical runtime. Codex is a supported compatibility
runtime under `adapters/codex/`. Gemini and Cursor remain experimental.
Adapters translate runtime form; they do not fork memory or contract meaning.

## Agents, skills, and commands

ATLAS ships a full specialist roster rather than a single generalist agent, so
work is routed to the responsibility that actually owns it:

| Component | Count | Location | Catalog |
| --- | --- | --- | --- |
| Agents | 87 | `.claude/agents/` | [Agent Catalog](docs/agent-catalog.md) |
| Skills | 126 | `.claude/skills/` | `.claude/registry.json` |
| Commands | 71 | `.claude/commands/` | `.claude/registry.json` |
| Workflows | 76 | `.claude/workflows/` | `.claude/registry.json` |
| Contracts | 6 | `.claude/contracts/` | `.claude/registry.json` |

Every agent's frontmatter `description` is both its routing signal for the
orchestrator and the hover/tooltip text Claude Code shows when selecting an
agent — there is no separate UI layer to maintain. `docs/agent-catalog.md` is
generated from that same frontmatter and should be regenerated whenever an
agent is added, renamed, or its description changes, so it never drifts from
the source of truth in `.claude/agents/`.

## Hooks

`.claude/hooks/hooks.json` mechanically enforces rules that would otherwise
only live in prose. Status: experimental — see
[Hook Contract](.claude/contracts/hook-contract.md) for what a hook must
declare before it ships, and how it differs from the six stable contracts.

Two hooks ship today, both scoped conservatively:

- `PreToolUse` (blocking): denies creating a new `.md`/`.txt` file directly at
  a project's root unless it's an allowlisted name (README, CLAUDE, AGENTS,
  CONTRIBUTING, CHANGELOG). Anything written inside a subdirectory —
  `docs/`, `.claude/`, or any other — is unaffected.
- `SessionEnd` (advisory, never blocks): reminds you to run
  `/atlas-checkpoint` or `/atlas-close-session` before a session's context is
  lost.

Because `.claude/hooks/hooks.json` is one of Claude Code's default plugin
component paths, both hooks are installed automatically for any project that
installs ATLAS as a plugin (see below) — not opt-in. To disable, remove or
edit `.claude/hooks/hooks.json` after installing.

## How execution works

ATLAS governs an AI coding runtime; it is not a standalone autonomous executor.
Claude Code can discover the root bootstrap, command prompts, rules, agent
definitions, and native skills. Markdown workflows, contracts, and review gates
are repository procedures that the selected runtime loads and interprets.
Python tools create and validate task, continuity, evidence, policy, and
release artifacts, but generated scaffolding must be reviewed and completed
with results that actually occurred.

See the [Daily Quickstart](docs/daily-quickstart.md) for one complete work cycle
and the [Operations Guide](docs/operations-guide.md) for the operating model.
For a disposable demonstration of the complete artifact lifecycle, use
`scripts/build_golden_path.py`; it does not execute product implementation.

## Install

For an empty or dedicated repository, extract the cumulative archive and copy
the contents of its versioned root into the target root. For an existing
project, do not bulk-overwrite files: run
`scripts/plan_project_adoption.py`, review every collision, and merge
project-owned files deliberately. The canonical hidden directory remains
`.claude/`.

For project-local, dedicated-repository, Windows, GitHub manual upload, and
incremental installation instructions, see [Installation](docs/installation.md).

### Install as a Claude Code plugin

ATLAS also installs through the Claude Code plugin marketplace, without
extracting or copying an archive. The repository root exposes
`.claude-plugin/marketplace.json`, which points to a single plugin (`atlas`)
sourced from `.claude/` — the same canonical directory used when Claude Code
is run directly inside this repository, so there is nothing to keep in sync.

```bash
claude plugin marketplace add <path-or-git-url-to-this-repo>
claude plugin install atlas@atlas-marketplace
```

Use `claude plugin details atlas@atlas-marketplace` to confirm the full
component inventory (agents, skills, commands, hooks) loaded. This path is
intended for making ATLAS available in *other* projects; a repository that
already has ATLAS under its own `.claude/` does not need to install it as a
plugin.

## Use with Claude Code

Claude Code loads `CLAUDE.md`, which imports the shared `AGENTS.md`
instructions. Start from the repository root, validate the continuity packet
and repository state, then use the closest command under `.claude/commands/`.
See the
[Claude Code Bootstrap Guide](docs/claude-code-bootstrap-guide.md).

## Use with Codex

Codex follows `AGENTS.md` and uses the adapter entry points under
`adapters/codex/commands/`. Generated catalogs and machine-readable maps point
back to the same canonical agents, skills, workflows, reviews, contracts, and
memory. Mappings preserve responsibility but still require Codex to interpret
the selected procedures. See the
[Codex Adoption Guide](docs/codex-adoption-guide.md).

## Validate

Install declared test dependencies:

```bash
python -m pip install --requirement requirements-test.txt
```

Use the portable validation runner. The quick profile checks foundational
structure; the full profile also checks runtime parity, native skill sync,
policies, documentation, and the complete test suite:

```bash
python scripts/validate_all.py --profile quick
python scripts/validate_all.py --profile full
```

Policy results are printed without rewriting the repository by default. The
GitHub Actions workflow runs the release validation profile on Python 3.12.

## Update manually

Incremental packages expose files intended for `.claude/` through:

```text
CLAUDE-DIRECTORY/
```

Copy those paths into `.claude/` in the installed repository. Apply only the
additions and replacements listed by the package, and remove only paths
explicitly named in `FILES-TO-DELETE.md`. Copying remains manual, but the
supported deployment process requires `scripts/manual_deploy_preflight.py`
before any add, replace, or delete. A conflict or `base_sha256` mismatch blocks
the patch and requires an explicit merge or a rebuilt package.

See the [Manual Deployment Guide](docs/manual-deployment-guide.md) and
[Framework Upgrade Guide](docs/framework-upgrade-guide.md).

## Build releases

```bash
python scripts/build_release.py --kind cumulative
python scripts/build_release.py --kind recovery
python scripts/build_incremental_release.py --base <directory-or-git-ref>
python scripts/validate_release_artifacts.py --archive <archive.zip>
```

Archives contain an internal content manifest. The final ZIP is verified by an
external checksum generated only after the archive is closed. In a Git
worktree, builders package tracked files plus untracked files that are not
ignored, subject to release exclusions; inspect `git status` because current
worktree content is authoritative. A symlink in the enumerated payload blocks
the build.

## Contribute

Read `AGENTS.md`, the canonical contracts, relevant memory, and the closest
workflow before changing the framework. Preserve established paths and
semantics, add validation proportional to risk, update documentation, and
record execution evidence. Do not commit secrets, caches, local reports, or
built archives.

## Support and limitations

- Claude Code: canonical, supported.
- Codex: compatibility runtime, supported.
- Gemini and Cursor: experimental.
- Runtime tool names and invocation differ by design.
- Local validation does not prove that GitHub-hosted CI has executed.
- Stable releases follow the support, compatibility, deprecation, audit, and
  rollback policies documented in this repository.

See [Support Policy](compatibility/support-policy.md),
[Runtime Matrix](compatibility/runtime-matrix.md), and
[Troubleshooting](docs/troubleshooting.md).
