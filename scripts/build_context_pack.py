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


def safe_project_file(relative: str) -> Path | None:
    candidate = (ROOT / relative).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    if not candidate.is_file():
        return None
    if (
        candidate.name in SECRET_NAMES
        or candidate.name.startswith(".env.")
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
    if runtime in {"claude", "claude-code"}:
        sources.append("adapters/claude/runtime-declaration.json")
    elif runtime == "codex":
        sources.append("adapters/codex/runtime-declaration.json")
    sources.extend(str(item) for item in envelope.get("affected_paths", []))
    return list(dict.fromkeys(sources))


def compose(
    envelope: dict,
    extra_sources: list[str],
    max_chars: int,
    max_total_chars: int,
) -> tuple[str, dict]:
    """Keep canonical instructions whole; defer optional files when budget is full."""
    route = canonical_sources({**envelope, "affected_paths": []})
    required = [name for name in route if name not in DOMAIN_MEMORY.get(str(envelope["task_type"]), [])]
    optional = list(dict.fromkeys([*envelope.get("affected_paths", []), *extra_sources]))
    stable = ["# Context Pack", "", "## Canonical sources", ""]
    missing: list[str] = []
    hashes: dict[str, str] = {}
    included: list[str] = []
    seen: set[str] = set()
    for name in route:
        path = safe_project_file(name)
        if path is None:
            if name in required:
                raise SystemExit(f"Required context source is unavailable: {name}")
            missing.append(name)
            continue
        normalized = path.relative_to(ROOT.resolve()).as_posix()
        if normalized in seen:
            continue
        seen.add(normalized)
        included.append(normalized)
        hashes[normalized] = hashlib.sha256(path.read_bytes()).hexdigest()
        stable.extend([f"### `{normalized}`", "", path.read_text(encoding="utf-8").rstrip(), ""])
    prefix = "\n".join(stable) + "\n"
    blocks: list[tuple[str, str]] = []
    truncated: list[str] = []
    for name in optional:
        path = safe_project_file(name)
        if path is None:
            missing.append(name)
            continue
        normalized = path.relative_to(ROOT.resolve()).as_posix()
        if normalized in seen:
            continue
        seen.add(normalized)
        text = path.read_text(encoding="utf-8")
        if len(text) > max_chars:
            truncated.append(normalized)
            text = text[:max_chars].rstrip() + "\n[Excerpt truncated; read the source before relying on omitted content.]"
        blocks.append((normalized, f"### `{normalized}`\n\n{text.rstrip()}\n"))
        hashes[normalized] = hashlib.sha256(path.read_bytes()).hexdigest()
    deferred: list[str] = []

    def render() -> str:
        array_fields = {"constraints", "acceptance_criteria", "affected_paths"}
        task = {
            key: envelope.get(key, [] if key in array_fields else "unspecified")
            for key in (
                "id", "task_type", "summary", "risk", "constraints",
                "acceptance_criteria", "affected_paths",
            )
        }
        limitations = {
            "missing_sources": missing,
            "deferred_sources": deferred,
            "truncated_sources": [name for name in truncated if name not in deferred],
            "selection": "heuristic; review relevant sources before execution",
        }
        return (
            prefix + "## Task (variable context)\n\n"
            + json.dumps(task, ensure_ascii=False, indent=2)
            + "\n\n## Task sources\n\n"
            + "\n".join(block for _, block in blocks)
            + "\n## Context limitations\n\n"
            + json.dumps(limitations, ensure_ascii=False, indent=2) + "\n"
        )

    content = render()
    while len(content) > max_total_chars and blocks:
        name, _ = blocks.pop()
        deferred.insert(0, name)
        content = render()
    if len(content) > max_total_chars:
        raise SystemExit(f"Context budget cannot fit mandatory instructions and task metadata ({len(content)} > {max_total_chars} characters); increase the budget or narrow the route")
    included.extend(name for name, _ in blocks)
    manifest = {
        "task_id": envelope["id"], "sources": included,
        "source_hashes": {name: hashes[name] for name in included},
        "missing_sources": list(dict.fromkeys(missing)), "deferred_sources": deferred,
        "truncated_sources": [name for name in truncated if name not in deferred],
        "selection": "canonical-prefix-plus-budgeted-task-sources",
        "context_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "stable_prefix_sha256": hashlib.sha256(prefix.encode("utf-8")).hexdigest(),
        "stable_prefix_chars": len(prefix), "rendered_chars": len(content),
        "max_total_chars": max_total_chars, "measurement_unit": "characters",
    }
    return content, manifest


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
    parser.add_argument("--max-chars", type=int, default=4000, help="Per optional source excerpt limit; characters, not tokens")
    parser.add_argument("--max-total-chars", type=int, default=64000, help="Hard limit for the complete rendered pack")
    parser.add_argument(
        "--no-update-envelope",
        action="store_true",
        help="Do not persist context_pack/context_manifest into the envelope.",
    )
    args = parser.parse_args()
    if args.max_chars < 200:
        raise SystemExit("--max-chars must be at least 200")

    if args.max_total_chars < 200:
        raise SystemExit("--max-total-chars must be at least 200")

    envelope_path = Path(args.task_envelope).resolve()
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))

    content, manifest = compose(envelope, args.source, args.max_chars, args.max_total_chars)

    output = (
        Path(args.output).resolve()
        if args.output
        else envelope_path.with_suffix(".context.md")
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(content.encode("utf-8"))

    manifest["context_pack"] = str(output)
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
