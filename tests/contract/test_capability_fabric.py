from __future__ import annotations

import json
from pathlib import Path

from scripts.discover_capabilities import discover
from scripts.generate_capability_fabric import build


ROOT = Path(__file__).resolve().parents[2]


def test_generated_catalog_matches_committed_artifacts() -> None:
    catalog, index = build()
    assert catalog == json.loads((ROOT / "atlas-registry/capabilities.json").read_text())
    assert index == json.loads((ROOT / "atlas-registry/ard-index.json").read_text())


def test_capability_ids_are_unique_and_paths_resolve() -> None:
    catalog, _ = build()
    capabilities = catalog["capabilities"]
    identifiers = [item["id"] for item in capabilities]
    assert len(identifiers) == len(set(identifiers))
    assert all((ROOT / item["path"]).is_file() for item in capabilities)
    assert all(item["trust"] == "internal" for item in capabilities)


def test_discovery_is_bounded_and_relevant() -> None:
    results = discover("browser security review", limit=3, kinds={"skill"})
    assert 0 < len(results) <= 3
    assert all(item["kind"] == "skill" for item in results)
    assert any("security" in item["id"] or "browser" in item["id"] for item in results)


def test_exact_name_has_highest_priority() -> None:
    results = discover("ai-search-measurement", limit=3, kinds={"skill"})
    assert results[0]["id"] == "skill:ai-search-measurement"
