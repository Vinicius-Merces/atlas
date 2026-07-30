from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = json.loads(
    (ROOT / ".claude" / "registry.json").read_text(encoding="utf-8")
)
GENERATED = json.loads(
    (
        ROOT
        / "adapters"
        / "codex"
        / "generated"
        / "catalog-manifest.json"
    ).read_text(encoding="utf-8")
)


def test_catalog_manifest_version_matches() -> None:
    assert GENERATED["version"] == REGISTRY["version"]


def test_generated_collection_counts_match_registry() -> None:
    for collection in ["agents", "commands", "skills", "workflows", "reviews"]:
        assert GENERATED["collections"][collection] == len(REGISTRY[collection])


def test_catalog_files_exist() -> None:
    base = ROOT / "adapters" / "codex" / "catalogs"
    for collection in ["agents", "commands", "skills", "workflows", "reviews"]:
        assert (base / f"{collection}.md").is_file()
