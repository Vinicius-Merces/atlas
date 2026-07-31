from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BASE_SOURCES = [
    "AGENTS.md",
    ".claude/memory/index.md",
    ".claude/memory/business.md",
    ".claude/memory/architecture.md",
    ".claude/contracts/agent-contract.md",
    ".claude/contracts/workflow-contract.md",
    ".claude/contracts/skill-contract.md",
    ".claude/contracts/review-contract.md",
]
DOMAIN_MEMORY = {
    "release": [".claude/memory/operations.md"],
    "security": [".claude/memory/security.md"],
    "privacy": [".claude/memory/security.md"],
    "integration": [".claude/memory/integrations.md"],
    "memory": [".claude/memory/contradictions.md"],
    "continuity": [".claude/memory/operations.md"],
}
SECRET_NAMES = {".env", "id_rsa", "id_ed25519"}


def excerpt(path: Path, limit: int) -> str:
    text = path.read_text(encoding="utf-8")
    return text[:limit].rstrip()


def safe_project_file(relative: str) -> Path | None:
    candidate = (ROOT / relative).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        return None
    if not candidate.is_file():
        return None
    if (
        candidate.name in SECRET_NAMES
        or candidate.suffix.lower() in {".pem", ".key"}
    ):
        return None
    return candidate


def canonical_sources(envelope: dict[str, object]) -> list[str]:
    sources = list(BASE_SOURCES)
    sources.extend(DOMAIN_MEMORY.get(str(envelope["task_type"]), []))

    roles = [
        str(envelope["primary_role"]),
        *[str(item) for item in envelope.get("supporting_roles", [])],
    ]
    sources.extend(f".claude/agents/{name}.md" for name in roles)
    sources.append(f".claude/workflows/{envelope['workflow']}.md")
    sources.extend(
        f".claude/skills/{name}/SKILL.md"
        for name in envelope.get("skills", [])
    )
    sources.extend(
        f".claude/reviews/{name}.md"
        for name in envelope.get("reviews", [])
    )
    runtime = str(envelope.get("runtime", ""))
    if runtime == "claude-code":
        sources.append("adapters/claude/runtime-declaration.json")
    elif runtime == "codex":
        sources.append("adapters/codex/runtime-declaration.json")
    sources.extend(str(item) for item in envelope.get("affected_paths", []))
    return list(dict.fromkeys(sources))


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Build a bounded ATLAS context pack from the routed task, its "
            "canonical capabilities, memory, and affected paths."
        )
    )
    parser.add_argument("--task-envelope", required=True)
    parser.add_argument("--output")
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="Additional repository file to include. Repeat as needed.",
    )
    parser.add_argument("--max-chars", type=int, default=4000)
    parser.add_argument(
        "--no-update-envelope",
        action="store_true",
        help="Do not persist context_pack/context_manifest into the envelope.",
    )
    args = parser.parse_args()
    if args.max_chars < 200:
        raise SystemExit("--max-chars must be at least 200")

    envelope_path = Path(args.task_envelope).resolve()
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))

    sections = [
        "# Context Pack",
        "",
        f"## Task",
        "",
        f"- ID: `{envelope['id']}`",
        f"- Type: `{envelope['task_type']}`",
        f"- Summary: {envelope['summary']}",
        f"- Risk: `{envelope.get('risk', 'unspecified')}`",
        f"- Primary role: `{envelope['primary_role']}`",
        f"- Workflow: `{envelope['workflow']}`",
        "",
        "## Canonical sources",
        "",
    ]

    included: list[str] = []
    hashes: dict[str, str] = {}
    missing: list[str] = []
    requested = [
        *canonical_sources(envelope),
        *args.source,
    ]
    for relative in list(dict.fromkeys(requested)):
        path = safe_project_file(relative)
        if path is not None:
            normalized = path.relative_to(ROOT).as_posix()
            included.append(normalized)
            hashes[normalized] = hashlib.sha256(path.read_bytes()).hexdigest()
            sections.extend([
                f"### `{normalized}`",
                "",
                excerpt(path, args.max_chars),
                "",
            ])
        else:
            missing.append(relative)

    sections.extend([
        "## Assumptions",
        "",
        "- Context selection is heuristic and should be reviewed before execution.",
        "",
        "## Missing context",
        "",
        *(
            [f"- `{item}`" for item in missing]
            if missing
            else ["- None detected from the requested source set."]
        ),
        "",
        "## Affected paths",
        "",
        *(
            [f"- `{item}`" for item in envelope.get("affected_paths", [])]
            if envelope.get("affected_paths")
            else ["- None declared."]
        ),
        "",
    ])

    output = (
        Path(args.output).resolve()
        if args.output
        else envelope_path.with_suffix(".context.md")
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(sections) + "\n", encoding="utf-8")

    manifest = {
        "task_id": envelope["id"],
        "context_pack": str(output),
        "sources": included,
        "source_hashes": hashes,
        "missing_sources": missing,
        "selection": "task-route-plus-explicit-paths",
    }
    manifest_path = output.with_suffix(".manifest.json")
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    if not args.no_update_envelope:
        try:
            context_reference = output.relative_to(ROOT).as_posix()
            manifest_reference = manifest_path.relative_to(ROOT).as_posix()
        except ValueError:
            context_reference = str(output)
            manifest_reference = str(manifest_path)
        envelope["context_pack"] = context_reference
        envelope["context_manifest"] = manifest_reference
        envelope["state"] = "context-ready"
        envelope_path.write_text(
            json.dumps(envelope, indent=2) + "\n",
            encoding="utf-8",
        )
    print(output)

if __name__ == "__main__":
    main()
