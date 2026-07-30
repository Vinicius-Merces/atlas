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
    "agents": ".claude/agents",
    "commands": ".claude/commands",
    "skills": ".claude/skills",
    "workflows": ".claude/workflows",
    "reviews": ".claude/reviews",
}


def render_catalog(title: str, items: list[str], canonical_root: str) -> str:
    lines = [
        f"# Codex {title} Catalog",
        "",
        "> Generated from `.claude/registry.json`. Do not edit manually.",
        "",
        f"Total: **{len(items)}**",
        "",
    ]
    for item in sorted(items):
        lines.append(f"- `{item}` → `{canonical_root}/{item}.md`")
    lines.append("")
    return "\n".join(lines)


def expected_outputs() -> dict[Path, str]:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    outputs: dict[Path, str] = {}

    for collection, canonical_root in COLLECTIONS.items():
        items = registry.get(collection, [])
        title = collection.capitalize()
        outputs[CATALOGS / f"{collection}.md"] = render_catalog(
            title, items, canonical_root
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
    }
    outputs[GENERATED / "catalog-manifest.json"] = (
        json.dumps(manifest, indent=2) + "\n"
    )
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    differences: list[str] = []
    for path, expected in expected_outputs().items():
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
