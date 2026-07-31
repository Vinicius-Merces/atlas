# ATLAS AI Engineering Framework

**Version:** `0.1.0-beta.12`
**Status:** Beta.12 hardening complete; hosted CI and independent RC approval pending

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

Claude Code is the canonical runtime. Codex is a beta-supported compatibility
runtime under `adapters/codex/`. Gemini and Cursor remain experimental.
Adapters translate runtime form; they do not fork memory or contract meaning.

## Install

For a clean installation, extract the cumulative archive and copy the contents
of its versioned root into the target repository. The canonical hidden
directory remains `.claude/`.

For project-local, dedicated-repository, Windows, GitHub manual upload, and
incremental installation instructions, see [Installation](docs/installation.md).

## Use with Claude Code

Start with `AGENTS.md`, `.claude/registry.json`, relevant project memory, and
the closest command under `.claude/commands/`. See the
[Claude Code Bootstrap Guide](docs/claude-code-bootstrap-guide.md).

## Use with Codex

Codex follows `AGENTS.md` and uses the adapter entry points under
`adapters/codex/commands/`. Generated catalogs and machine-readable maps point
back to the same canonical agents, skills, workflows, reviews, contracts, and
memory. See the [Codex Adoption Guide](docs/codex-adoption-guide.md).

## Validate

Install declared test dependencies:

```bash
python -m pip install --requirement requirements-test.txt
```

Run the primary gates:

```bash
python scripts/manage_version.py
python scripts/validate_registry.py
python scripts/validate_package.py
python scripts/validate_contracts.py
python scripts/validate_schemas.py
python scripts/validate_codex_adapter.py
python scripts/detect_runtime_drift.py
python scripts/validate_source_of_truth.py
python scripts/validate_memory_freshness.py --strict
python scripts/evaluate_policies.py
python -m pytest tests -q
```

The GitHub Actions workflow runs the full validation chain on Python 3.12.

## Update manually

Incremental packages expose files intended for `.claude/` through:

```text
CLAUDE-DIRECTORY/
```

Copy those paths into `.claude/` in the installed repository. Apply only the
additions and replacements listed by the package, and remove only paths
explicitly named in `FILES-TO-DELETE.md`. No script is required to apply a
patch; validators and simulators are optional safety tools.

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
external checksum generated only after the archive is closed.

## Contribute

Read `AGENTS.md`, the canonical contracts, relevant memory, and the closest
workflow before changing the framework. Preserve established paths and
semantics, add validation proportional to risk, update documentation, and
record execution evidence. Do not commit secrets, caches, local reports, or
built archives.

## Support and limitations

- Claude Code: canonical, beta-supported.
- Codex: compatibility runtime, beta-supported.
- Gemini and Cursor: experimental.
- Runtime tool names and invocation differ by design.
- Local validation does not prove that GitHub-hosted CI has executed.
- Stable `0.1.0` is not authorized until the RC and stable checklists pass.

See [Support Policy](compatibility/support-policy.md),
[Runtime Matrix](compatibility/runtime-matrix.md), and
[Troubleshooting](docs/troubleshooting.md).
