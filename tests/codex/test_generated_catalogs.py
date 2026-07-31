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


def test_machine_readable_maps_are_complete_and_resolvable() -> None:
    generated = ROOT / "adapters" / "codex" / "generated"
    required_fields = {
        "canonical_name",
        "canonical_path",
        "adapter_path",
        "parity_type",
        "status",
        "notes",
        "version",
    }
    for collection, map_name in GENERATED["maps"].items():
        data = json.loads((generated / map_name).read_text(encoding="utf-8"))
        entries = data["entries"]
        assert data["collection"] == collection
        assert len(entries) == len(REGISTRY[collection])
        assert {entry["canonical_name"] for entry in entries} == set(
            REGISTRY[collection]
        )
        for entry in entries:
            assert required_fields <= entry.keys()
            assert (ROOT / entry["canonical_path"]).is_file()
            assert (ROOT / entry["adapter_path"]).is_file()
            assert entry["version"] == REGISTRY["version"]


def test_all_claude_agents_use_the_canonical_runtime_directory() -> None:
    data = json.loads(
        (
            ROOT / "adapters" / "codex" / "generated" / "agent-map.json"
        ).read_text(encoding="utf-8")
    )
    assert not (ROOT / "agents").exists()
    for entry in data["entries"]:
        assert entry["canonical_path"].startswith(".claude/agents/")
