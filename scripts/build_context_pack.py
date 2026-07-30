from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CANDIDATES = [
    ".claude/memory/business.md",
    ".claude/memory/architecture.md",
    ".claude/memory/integrations.md",
    ".claude/memory/security.md",
    "README.md",
    "docs/INDEX.md",
]

def excerpt(path: Path, limit: int = 4000) -> str:
    text = path.read_text(encoding="utf-8")
    return text[:limit].rstrip()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-envelope", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    envelope_path = Path(args.task_envelope)
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))

    sections = [
        "# Context Pack",
        "",
        f"## Task",
        "",
        f"- ID: `{envelope['id']}`",
        f"- Type: `{envelope['task_type']}`",
        f"- Summary: {envelope['summary']}",
        f"- Primary role: `{envelope['primary_role']}`",
        f"- Workflow: `{envelope['workflow']}`",
        "",
        "## Canonical sources",
        "",
    ]

    included = []
    for relative in CANDIDATES:
        path = ROOT / relative
        if path.is_file():
            included.append(relative)
            sections.extend([
                f"### `{relative}`",
                "",
                excerpt(path),
                "",
            ])

    sections.extend([
        "## Assumptions",
        "",
        "- Context selection is heuristic and should be reviewed before execution.",
        "",
        "## Missing context",
        "",
        "- Add task-specific repository paths, ADRs, and constraints when required.",
        "",
    ])

    output = Path(args.output) if args.output else envelope_path.with_suffix(".context.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(sections), encoding="utf-8")

    manifest = {
        "task_id": envelope["id"],
        "context_pack": str(output),
        "sources": included,
    }
    output.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)

if __name__ == "__main__":
    main()
