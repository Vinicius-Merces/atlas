from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "adapters" / "codex" / "runtime-manifest.json"


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_codex_version_matches_framework() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert load_manifest()["version"] == version


def test_codex_is_beta_supported() -> None:
    assert load_manifest()["support"] == "beta-supported"


def test_codex_collections_exist() -> None:
    base = ROOT / "adapters" / "codex"
    for relative in load_manifest()["collections"].values():
        assert (base / relative).exists(), relative
