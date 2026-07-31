from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"
CODEX = ROOT / "adapters" / "codex"
CATALOGS = CODEX / "catalogs"
GENERATED = CODEX / "generated"


COLLECTIONS = {
    "agents": (".claude/agents",),
    "commands": (".claude/commands",),
    "skills": (".claude/skills",),
    "workflows": (".claude/workflows",),
    "reviews": (".claude/reviews",),
}

MAP_NAMES = {
    "agents": "agent-map.json",
    "commands": "command-map.json",
    "skills": "skill-map.json",
    "workflows": "workflow-map.json",
    "reviews": "review-map.json",
}


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def resolve_registered_paths(
    collection: str, items: list[str], canonical_roots: tuple[str, ...]
) -> dict[str, Path]:
    candidates: dict[str, list[Path]] = {}
    for canonical_root in canonical_roots:
        for path in (ROOT / canonical_root).rglob("*.md"):
            if collection == "skills":
                if path.name != "SKILL.md":
                    continue
                name = path.parent.name
            else:
                name = path.stem
            candidates.setdefault(name, []).append(path)

    resolved: dict[str, Path] = {}
    errors: list[str] = []
    for item in items:
        matches = candidates.get(item, [])
        if len(matches) == 1:
            resolved[item] = matches[0]
        elif not matches:
            errors.append(f"{collection}:{item} has no canonical Markdown file")
        else:
            paths = ", ".join(relative(path) for path in sorted(matches))
            errors.append(f"{collection}:{item} is ambiguous: {paths}")

    if errors:
        raise ValueError("\n".join(errors))
    return resolved


def resolve_adapter_path(collection: str, item: str) -> Path | None:
    if collection == "skills":
        native = ROOT / ".agents" / "skills" / item / "SKILL.md"
        return native if native.is_file() else None
    matches = [
        path
        for path in (CODEX / collection).rglob("*.md")
        if path.stem == item
    ]
    if len(matches) > 1:
        paths = ", ".join(relative(path) for path in sorted(matches))
        raise ValueError(f"Codex adapter path for {collection}:{item} is ambiguous: {paths}")
    return matches[0] if matches else None


def render_catalog(title: str, resolved: dict[str, Path]) -> str:
    lines = [
        f"# Codex {title} Catalog",
        "",
        "> Generated from `.claude/registry.json`. Do not edit manually.",
        "",
        f"Total: **{len(resolved)}**",
        "",
    ]
    for item, path in sorted(resolved.items()):
        lines.append(f"- `{item}` → `{relative(path)}`")
    lines.append("")
    return "\n".join(lines)


def expected_outputs() -> dict[Path, str]:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    outputs: dict[Path, str] = {}

    for collection, canonical_roots in COLLECTIONS.items():
        items = registry.get(collection, [])
        resolved = resolve_registered_paths(collection, items, canonical_roots)
        title = collection.capitalize()
        outputs[CATALOGS / f"{collection}.md"] = render_catalog(title, resolved)

        entries = []
        for item, canonical_path in sorted(resolved.items()):
            adapter_path = resolve_adapter_path(collection, item)
            is_native = adapter_path is not None
            entries.append(
                {
                    "canonical_name": item,
                    "canonical_path": relative(canonical_path),
                    "adapter_path": (
                        relative(adapter_path)
                        if adapter_path
                        else f"adapters/codex/catalogs/{collection}.md"
                    ),
                    "parity_type": (
                        "runtime-native" if is_native else "canonical-reference"
                    ),
                    "status": "native" if is_native else "mapped",
                    "notes": (
                        "Codex-native entry point."
                        if is_native
                        else "Resolved through the generated catalog to the canonical source."
                    ),
                    "version": registry["version"],
                }
            )

        map_data = {
            "version": registry["version"],
            "generated_from": ".claude/registry.json",
            "collection": collection,
            "entries": entries,
        }
        outputs[GENERATED / MAP_NAMES[collection]] = (
            json.dumps(map_data, indent=2) + "\n"
        )

    index_lines = [
        "# Codex Generated Runtime Index",
        "",
        "> Generated from the canonical ATLAS registry.",
        "",
    ]
    for collection in COLLECTIONS:
        count = len(registry.get(collection, []))
        index_lines.append(
            f"- [{collection.capitalize()}](../catalogs/{collection}.md): {count}"
        )
    index_lines.append("")
    outputs[GENERATED / "INDEX.md"] = "\n".join(index_lines)

    manifest = {
        "version": registry["version"],
        "generated_from": ".claude/registry.json",
        "collections": {
            name: len(registry.get(name, [])) for name in COLLECTIONS
        },
        "maps": MAP_NAMES,
    }
    outputs[GENERATED / "catalog-manifest.json"] = (
        json.dumps(manifest, indent=2) + "\n"
    )
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    try:
        outputs = expected_outputs()
    except ValueError as exc:
        print("Codex adapter generation failed:")
        for error in str(exc).splitlines():
            print(f"- {error}")
        raise SystemExit(1) from None

    differences: list[str] = []
    for path, expected in outputs.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != expected:
            differences.append(str(path.relative_to(ROOT)))
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(expected, encoding="utf-8")

    if args.check and differences:
        print("Codex adapter is out of sync:")
        for item in differences:
            print(f"- {item}")
        raise SystemExit(1)

    if differences:
        print(f"Synchronized {len(differences)} generated files.")
    else:
        print("Codex adapter catalogs are synchronized.")


if __name__ == "__main__":
    main()
