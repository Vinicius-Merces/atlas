from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / ".claude" / "registry.json"


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

    list_fields = ["agents", "contracts", "skills", "reviews", "workflows", "commands"]
    for field in list_fields:
        values = registry.get(field, [])
        if not isinstance(values, list):
            fail(f"Registry field '{field}' must be a list")
        duplicates = sorted({item for item in values if values.count(item) > 1})
        if duplicates:
            fail(f"Duplicate entries in '{field}': {', '.join(duplicates)}")

    print(f"Registry valid: {registry['version']}")


if __name__ == "__main__":
    main()
