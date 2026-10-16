# Project-local memory

Product knowledge belongs to the product repository. ATLAS upstream stores the
framework's code, contracts and its own engineering state; it is not an aggregator
of product sessions, decisions or customer data.

## One entry point, explicit destination

The toolkit may live outside the product. Always pass the product's exact Git root:

```bash
python /path/to/atlas/scripts/project_memory.py init --project-root /path/to/product
python /path/to/atlas/scripts/project_memory.py start --project-root /path/to/product
```

`init` creates a project identity in `.atlas/project-memory.json`, preserves
existing canonical project memory, initializes continuity, and generates a local
Obsidian view. It is idempotent for an already initialized project. No product
`VERSION`, `README.md`, application source or framework checkout is overwritten.
The framework version is kept separately from the product version.

The tool requires a Git root and refuses the upstream ATLAS repository as a product
target. It binds the project to its origin when one exists, recording only an origin
fingerprint. An origin rename or migration requires reviewed identity reconciliation.
Without an origin, identity relies on the local project marker; copying that marker
is not a supported way to initialize another project. These guards prevent accidental
mixing, not adversarial modification of files by someone with write access.

## Where knowledge lives

| Path inside each product | Responsibility |
| --- | --- |
| `.claude/memory/` | Canonical validated facts and durable decisions, shared across runtimes |
| `.atlas/continuity/` | Latest session, project brief, resume packet and archived sessions |
| `.atlas/project-memory.json` | Project identity, framework version and generated view checksum |
| `obsidian/atlas-project/Project Memory.md` | Generated read-only view of that project's memory and current session |

Open the product's `obsidian/` folder as a vault. The generated Markdown contains
actual local memory content and does not require links outside the vault to read
that content. Its filename and folder are stable; treat it as a derived view and
edit canonical `.claude/memory/` files. Native Obsidian UI rendering is not tested
by the CLI; filesystem isolation and content are covered by automated tests.

## Close and resume

1. Record only verified stable facts in the product's `.claude/memory/` files.
2. Copy/edit its latest session into `.atlas/continuity/staged-session.json`,
   preserving `project_id` and `framework_version`; use a new `session_id` for a
   new session. Fill actual changed files, checks, decisions, pending work and risks.
3. Run:

```bash
python /path/to/atlas/scripts/project_memory.py close --project-root /path/to/product --session-file /path/to/product/.atlas/continuity/staged-session.json
python /path/to/atlas/scripts/project_memory.py start --project-root /path/to/product
```

Close validates the session schema and identity, preserves the previous session,
rebuilds briefs/resume packet through the canonical builders, validates continuity,
and refreshes the Obsidian view. A foreign session or manually edited view is
rejected rather than overwritten. Start is read-only and provides resume context
from that project's files in a new process. It does not implement pending work or
independently verify claimed product test results.

Start reports current canonical memory paths even if new notes were added after
the previous closeout. `obsidian_status` identifies a current, stale, edited or
missing view. A stale view can be refreshed through close; an edited view requires
preserving the edits in canonical memory first.

Commit the product-owned memory and continuity in the product's Git repository
when persistence is authorized. Local file creation alone does not push to GitHub.
Do not store secrets or participant/customer personal data in these artifacts.

## Adoption and legacy state

The adoption planner excludes upstream `.claude/memory/` knowledge (templates
remain distributable) and upstream `obsidian/atlas/` indexes. Initialize product
memory after merging framework instructions; never copy the framework's own
session state into a product. Updates must preserve product-owned memory.
The planner also excludes generated product views and rejects a product-bound
repository as the framework distribution source.

Existing unbound continuity or detected copied framework memory requires manual
reconciliation before initialization. Review and archive old state inside the
product, remove only confirmed foreign copies, and then initialize. The command
does not erase legacy state or migrate real projects automatically.

Existing low-level builders remain available for framework maintenance. For product
work, use this explicit entry point. Runtime instructions must invoke start/close;
this is a deterministic lifecycle command, not a background recorder or a guarantee
that mentioning ATLAS in arbitrary chat executes a local command.
