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
