from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / ".claude" / "registry.json"
COLLECTION_ROOTS = {
    "agents": (".claude/agents",),
    "contracts": (".claude/contracts",),
    "skills": (".claude/skills",),
    "reviews": (".claude/reviews",),
    "workflows": (".claude/workflows",),
    "commands": (".claude/commands",),
}


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> None:
    if not REGISTRY_PATH.exists():
        fail(f"Missing registry: {REGISTRY_PATH}")

    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"Invalid registry JSON: {exc}")

    required = ["version", "orchestrator", "agents", "contracts", "workflows"]
    missing = [key for key in required if key not in registry]
    if missing:
        fail(f"Missing required registry keys: {', '.join(missing)}")

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if registry["version"] != version:
        fail(
            f"Registry version {registry['version']} does not match VERSION {version}"
        )

    list_fields = ["agents", "contracts", "skills", "reviews", "workflows", "commands"]
    for field in list_fields:
        values = registry.get(field, [])
        if not isinstance(values, list):
            fail(f"Registry field '{field}' must be a list")
        invalid = [item for item in values if not isinstance(item, str) or not item]
        if invalid:
            fail(f"Registry field '{field}' contains invalid names")
        duplicates = sorted({item for item in values if values.count(item) > 1})
        if duplicates:
            fail(f"Duplicate entries in '{field}': {', '.join(duplicates)}")

        candidates: dict[str, list[Path]] = {}
        for relative_root in COLLECTION_ROOTS[field]:
            for path in (ROOT / relative_root).rglob("*.md"):
                candidates.setdefault(path.stem, []).append(path)
        for item in values:
            matches = candidates.get(item, [])
            if not matches:
                fail(f"Registered {field} item has no file: {item}")
            if len(matches) > 1:
                paths = ", ".join(
                    path.relative_to(ROOT).as_posix() for path in sorted(matches)
                )
                fail(f"Registered {field} item is ambiguous: {item}: {paths}")

    orchestrator_matches = [
        path
        for relative_root in COLLECTION_ROOTS["agents"]
        for path in (ROOT / relative_root).rglob("*.md")
        if path.stem == registry["orchestrator"]
    ]
    if len(orchestrator_matches) != 1:
        fail(
            "Registry orchestrator must resolve to exactly one agent file: "
            f"{registry['orchestrator']}"
        )

    print(f"Registry valid: {registry['version']}")


if __name__ == "__main__":
    main()
