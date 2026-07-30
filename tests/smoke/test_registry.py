from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_registry_version_matches_version_file() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    registry = json.loads((ROOT / ".claude" / "registry.json").read_text(encoding="utf-8"))
    assert registry["version"] == version


def test_registry_has_core_collections() -> None:
    registry = json.loads((ROOT / ".claude" / "registry.json").read_text(encoding="utf-8"))
    for key in ["agents", "skills", "reviews", "workflows", "commands", "contracts"]:
        assert key in registry
        assert isinstance(registry[key], list)
