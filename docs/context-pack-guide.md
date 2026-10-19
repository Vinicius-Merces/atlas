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
select relevant files explicitly. Large optional Markdown files are ranked by
heading/section terms and Python files by AST function/class names and bodies,
using the task summary, constraints and acceptance criteria. This is deterministic
lexical selection, not embeddings or a semantic completeness guarantee. Other
formats, invalid Python and unmatched queries fall back to a disclosed prefix.
Sections or symbols larger than the limit may be cut and remain excerpts; never
treat them as complete instructions or executable code. Inspect omitted content
before making decisions that depend on it. `--selection prefix` retains the
baseline behavior for controlled comparisons.

Explicitly selected AGENTS.md, CLAUDE.md, SKILL.md and instruction directories
are promoted to the mandatory full-source prefix. They cannot be shortened to
make the budget fit. Source-range labels and limitations count toward the global
budget; lower-priority optional files may still be deferred.

## Project-local extraction reuse

The default disposable cache is `.atlas/cache/context-extractions/` inside the
selected project. It stores only selected character ranges, strategy and an
integrity checksum, not source text, answers, tool outputs or prompt content.
Every build still reads and hashes full current source bytes. Reuse avoids
repeating parsing and lexical ranking; it does not avoid reading the source or
prove faster end-to-end tasks.

Cache keys include the resolved project root, initialized project identity when
present, relative source path, full content hash, normalized query terms, per-file
budget, mode and extractor version. Changes outside the excerpt invalidate reuse.
Copied cache entries are not reused in another project. Corrupt entries are
recomputed from source; unsafe symlink locations are bypassed. Writes use a
temporary file and atomic replacement. Cache contents are local, ignored by Git,
derived and disposable; they are never canonical memory or Obsidian knowledge.

Use `--no-cache` to disable reads and writes. Old entries are not automatically
pruned; the project owner may discard the derived cache directory when needed.
The manifest reports hit/miss/bypassed **extraction counts**, not provider cache
hits, token savings, latency improvement or financial savings. Warm/cold content
bytes remain identical; diagnostics can differ.

For an adopted product using the toolkit from elsewhere, explicitly select that
product for build, verification and planning:

```bash
python /path/to/atlas/scripts/build_context_pack.py --project-root /path/to/product --task-envelope /path/to/product/task.json
python /path/to/atlas/scripts/validate_context_pack.py --project-root /path/to/product --manifest /path/to/product/task.context.manifest.json --context-pack /path/to/product/task.context.md --task-id task-example
python /path/to/atlas/scripts/build_execution_plan.py --project-root /path/to/product --task-envelope /path/to/product/task.json --runtime codex
```

All canonical sources must exist in the selected product; missing instructions
never fall back to upstream toolkit memory. Explicit product tasks and output
paths must remain local. The builder refuses to overwrite its task or input
sources. Initialize/resume product memory through the existing project-memory
entry point first; these context commands do not create or migrate memories.

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

New manifests bind the pack to its resolved project root and map optional source
ranges to current character offsets and line numbers. Verification reconstructs
each excerpt from current source bytes and checks the range map, excerpt digest,
presence in the pack and declared per-source budget. Moving a pack to another
checkout requires a local rebuild. The planner also verifies a hash of current
task inputs (including summary, criteria, constraints and routing); editing the
same task ID requires rebuilding. Standalone verification can apply that check
with `--task-envelope task.json` in addition to `--task-id`.
Legacy manifests retain their earlier
verification behavior; rebuild to obtain the new range/project metadata.

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
