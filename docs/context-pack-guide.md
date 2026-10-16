# Context Pack Guide

Context packs are derived, source-linked snapshots. They reduce initial context;
they do not enable provider prompt caching, enlarge a model window, or establish
that every relevant source has been read.

## Build with a global budget

```bash
python scripts/build_context_pack.py --task-envelope task.json --max-total-chars 64000 --max-chars 4000
```

`--max-total-chars` caps the entire rendered Markdown, including headings, task
constraints, acceptance criteria and limitation lists. The unit is Unicode
characters, not tokens. `--max-chars` limits each optional source excerpt.
Canonical instructions, selected roles, workflows, reviews and skills are kept
whole. If they and the task metadata cannot fit, construction fails before writing
outputs. Narrow the route or explicitly increase the budget; do not silently
remove mandatory rules.

Optional sources are considered in affected-path order, followed by explicit
`--source` order, deduplicated by resolved path. Lower-priority files are deferred
from the end until the pack fits. Missing sources, deferred files and truncated
excerpts are disclosed in both pack and manifest. Directories are not expanded;
select relevant files explicitly. Prefix excerpts remain heuristic: inspect omitted
content before making decisions that depend on it.

## Stable and variable content

Canonical source content comes first in deterministic route order. Task ID,
summary, risk, constraints, acceptance criteria and task files follow. The manifest
records a separate hash and length for the stable prefix. This layout supports
prefix reuse when a compatible runtime controls request assembly; it does not
prove a provider cache hit. No prewarming requests or external API calls are made.

## Verify before planning

```bash
python scripts/validate_context_pack.py --manifest task.context.manifest.json --context-pack task.context.md --task-id TASK_ID
python scripts/build_execution_plan.py --task-envelope task.json --runtime codex
```

The planner checks the explicit manifest or the pack's sibling `.manifest.json`.
It verifies task identity, pack reference, exact bytes, character budget, prefix
hash and all included source hashes. A change anywhere in a source, including
beyond an excerpt, requires rebuilding. References outside the repository and
removed sources are rejected. Reverify after repository changes and before using
a retained plan; the planner cannot freeze future filesystem state.

`context_verified` means integrity and freshness were checked, not semantic
completeness. `context_limitations` carries missing, deferred and truncated sources.
Review those limitations and load additional relevant content before execution.
Hashes detect accidental drift against the manifest; they do not authenticate an
untrusted manifest or make arbitrary content safe.

## Migration

Rebuild existing packs to obtain the integrity and budget metadata. For a manually
assembled legacy pack without a manifest, `--allow-unverified-context` produces an
explicitly unverified draft. It cannot bypass an existing manifest that fails
verification. `--allow-missing-context` remains an explicit context-free draft mode.
Neither option establishes readiness for implementation or relaxes review gates.

See [Context efficiency plan](context-efficiency-plan.md) for subsequent semantic
selection, local extraction reuse and measured runtime integration.
