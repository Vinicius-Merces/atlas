from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

if __package__:
    from .context_extraction import extract, terms, task_digest
else:
    from context_extraction import extract, terms, task_digest

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


def safe_project_file(relative: str, root: Path | None = None) -> Path | None:
    root = (root or ROOT).resolve()
    original = root / relative
    candidate = original.resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    if not candidate.is_file():
        return None
    if any(p.is_symlink() for p in [original, *original.parents] if p.is_relative_to(root)):
        return None
    if (
        candidate.name in SECRET_NAMES
        or candidate.name.startswith(".env.")
        or candidate.suffix.lower() in {".pem", ".key"}
    ):
        return None
    return candidate


def instruction_source(name: str) -> bool:
    path = Path(name)
    return path.name in {"AGENTS.md", "CLAUDE.md", "SKILL.md"} or any(
        part in {"contracts", "rules", "agents", "workflows", "reviews"} for part in path.parts
    )


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
    *,
    root: Path | None = None,
    use_cache: bool = True,
    selection_mode: str = "relevant",
) -> tuple[str, dict]:
    """Keep canonical instructions whole; defer optional files when budget is full."""
    root = (root or ROOT).resolve()
    if max_chars < 200 or max_total_chars < 200 or selection_mode not in {"relevant", "prefix"}:
        raise ValueError("Invalid context budget or selection mode")
    route = canonical_sources({**envelope, "affected_paths": []})
    required = [name for name in route if name not in DOMAIN_MEMORY.get(str(envelope["task_type"]), [])]
    optional = list(dict.fromkeys([*envelope.get("affected_paths", []), *extra_sources]))
    for name in optional:
        if instruction_source(name) and name not in route:
            route.append(name)
            required.append(name)
    stable = ["# Context Pack", "", "## Canonical sources", ""]
    missing: list[str] = []
    hashes: dict[str, str] = {}
    included: list[str] = []
    seen: set[str] = set()
    for name in route:
        path = safe_project_file(name, root)
        if path is None:
            if name in required:
                raise SystemExit(f"Required context source is unavailable: {name}")
            missing.append(name)
            continue
        normalized = path.relative_to(root).as_posix()
        if normalized in seen:
            continue
        seen.add(normalized)
        included.append(normalized)
        raw = path.read_bytes()
        hashes[normalized] = hashlib.sha256(raw).hexdigest()
        stable.extend([f"### `{normalized}`", "", raw.decode("utf-8").rstrip(), ""])
    prefix = "\n".join(stable) + "\n"
    blocks: list[tuple[str, str]] = []
    truncated: list[str] = []
    excerpts: dict[str, dict] = {}
    cache_counts = {"hit": 0, "miss": 0, "bypassed": 0}
    query = terms(" ".join([str(envelope.get("summary", "")),
                           *map(str, envelope.get("constraints", [])),
                           *map(str, envelope.get("acceptance_criteria", []))]))
    for name in optional:
        path = safe_project_file(name, root)
        if path is None:
            missing.append(name)
            continue
        normalized = path.relative_to(root).as_posix()
        if normalized in seen:
            continue
        seen.add(normalized)
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        hashes[normalized] = hashlib.sha256(raw).hexdigest()
        if len(text) > max_chars:
            truncated.append(normalized)
        text, metadata, cache_state = extract(root, normalized, text, hashes[normalized], query,
                                               max_chars, use_cache=use_cache, mode=selection_mode)
        excerpts[normalized] = metadata
        cache_counts[cache_state] += 1
        blocks.append((normalized, f"### `{normalized}`\n\n{text.rstrip()}\n"))
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
        "selection": "canonical-prefix-plus-budgeted-selected-ranges",
        "source_excerpts": {name: excerpts[name] for name, _ in blocks},
        "extraction_cache": cache_counts,
        "extraction_max_chars": max_chars,
        "project_root_sha256": hashlib.sha256(str(root).encode()).hexdigest(),
        "task_inputs_sha256": task_digest(envelope),
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
    parser.add_argument("--project-root", type=Path, help="Explicit adopted product root; never falls back to toolkit sources")
    parser.add_argument("--selection", choices=["relevant", "prefix"], default="relevant")
    parser.add_argument("--no-cache", action="store_true", help="Disable local extraction-cache reads and writes")
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
    root = args.project_root.resolve(strict=True) if args.project_root else ROOT
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))

    output = (
        Path(args.output).resolve()
        if args.output
        else envelope_path.with_suffix(".context.md")
    )
    if args.project_root and (not envelope_path.is_relative_to(root) or not output.is_relative_to(root)):
        raise SystemExit("Task and context output must remain inside the explicit project root")
    if output == envelope_path or output.with_suffix(".manifest.json") == envelope_path:
        raise SystemExit("Context output cannot overwrite its task envelope")
    protected = {(root / name).resolve() for name in [*canonical_sources(envelope), *args.source]}
    if output in protected or output.with_suffix(".manifest.json") in protected:
        raise SystemExit("Context output cannot overwrite an input source")
    content, manifest = compose(envelope, args.source, args.max_chars, args.max_total_chars,
                                root=root, use_cache=not args.no_cache, selection_mode=args.selection)
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
            context_reference = output.relative_to(root).as_posix()
            manifest_reference = manifest_path.relative_to(root).as_posix()
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
