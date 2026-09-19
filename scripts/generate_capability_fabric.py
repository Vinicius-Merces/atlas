#!/usr/bin/env python3
"""Generate compact capability discovery artifacts from canonical ATLAS sources."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"
OUTPUT = ROOT / "atlas-registry"
COLLECTIONS = {
    "agents": ("agent", ROOT / ".claude" / "agents", ".md"),
    "skills": ("skill", ROOT / ".claude" / "skills", "SKILL.md"),
    "workflows": ("workflow", ROOT / ".claude" / "workflows", ".md"),
    "reviews": ("review", ROOT / ".claude" / "reviews", ".md"),
    "commands": ("command", ROOT / ".claude" / "commands", ".md"),
}
TOKEN = re.compile(r"[a-z0-9]+")


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    raw, separator, _ = text[4:].partition("\n---\n")
    if not separator:
        raise ValueError(f"Unterminated frontmatter: {path.relative_to(ROOT)}")
    parsed = yaml.safe_load(raw)
    return parsed if isinstance(parsed, dict) else {}


def resolve_path(collection: str, name: str) -> Path:
    _, base, suffix = COLLECTIONS[collection]
    path = base / name / suffix if collection == "skills" else base / f"{name}{suffix}"
    if not path.is_file():
        raise ValueError(f"Missing canonical capability: {path.relative_to(ROOT)}")
    return path


def fallback_description(kind: str, name: str) -> str:
    return f"ATLAS {kind} capability for {name.replace('-', ' ')}."


def keywords(name: str, description: str) -> list[str]:
    name_tokens = TOKEN.findall(name.lower())
    description_tokens = TOKEN.findall(description.lower())
    useful = [token for token in [*name_tokens, *description_tokens] if len(token) > 2]
    return sorted(dict.fromkeys(useful))[:24]


def build() -> tuple[dict[str, object], dict[str, object]]:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    capabilities: list[dict[str, object]] = []
    for collection, (kind, _, _) in COLLECTIONS.items():
        names = list(registry.get(collection, []))
        if collection == "agents" and registry["orchestrator"] not in names:
            names.append(registry["orchestrator"])
        for name in names:
            path = resolve_path(collection, name)
            metadata = frontmatter(path)
            description = metadata.get("description")
            if not isinstance(description, str) or not description.strip():
                description = fallback_description(kind, name)
            description = " ".join(description.split())
            capabilities.append(
                {
                    "id": f"{kind}:{name}",
                    "name": name,
                    "kind": kind,
                    "description": description,
                    "path": path.relative_to(ROOT).as_posix(),
                    "keywords": keywords(name, description),
                    "trust": "internal",
                }
            )
    capabilities.sort(key=lambda item: str(item["id"]))
    catalog = {
        "schema_version": 1,
        "atlas_version": registry["version"],
        "generated_from": ".claude/registry.json",
        "capabilities": capabilities,
    }
    index = {
        "schema_version": 1,
        "atlas_version": registry["version"],
        "generated_from": "atlas-registry/capabilities.json",
        "default_limit": 3,
        "capabilities": [
            {
                "id": item["id"],
                "kind": item["kind"],
                "description": item["description"],
                "keywords": item["keywords"],
                "path": item["path"],
                "trust": item["trust"],
            }
            for item in capabilities
        ],
    }
    return catalog, index


def render(value: dict[str, object]) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    catalog, index = build()
    outputs = {
        OUTPUT / "capabilities.json": render(catalog),
        OUTPUT / "ard-index.json": render(index),
    }
    stale: list[str] = []
    for path, content in outputs.items():
        if args.check:
            if not path.is_file() or path.read_text(encoding="utf-8") != content:
                stale.append(path.relative_to(ROOT).as_posix())
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(f"Generated {path.relative_to(ROOT)}")
    if stale:
        print("Stale capability fabric artifacts:")
        for path in stale:
            print(f"- {path}")
        return 1
    if args.check:
        print(f"Capability fabric is current: {len(catalog['capabilities'])} capabilities")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
