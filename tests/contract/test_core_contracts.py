from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "compatibility" / "core-contracts.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_manifest_version_matches_framework() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert load_manifest()["version"] == version


def test_all_contract_files_exist() -> None:
    for contract in load_manifest()["contracts"]:
        assert (ROOT / contract["path"]).is_file(), contract["path"]


def test_all_canonical_paths_exist() -> None:
    for relative in load_manifest()["canonical_paths"]:
        assert (ROOT / relative).exists(), relative


def test_contract_status_matches_release_stability() -> None:
    manifest = load_manifest()
    expected = f"stable-{manifest['stability']}"
    for contract in load_manifest()["contracts"]:
        assert contract["status"] == expected
