from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = json.loads(
    (ROOT / ".claude" / "registry.json").read_text(encoding="utf-8")
)


def test_every_registered_item_appears_in_codex_catalog() -> None:
    base = ROOT / "adapters" / "codex" / "catalogs"
    for collection in ["agents", "commands", "skills", "workflows", "reviews"]:
        text = (base / f"{collection}.md").read_text(encoding="utf-8")
        for item in REGISTRY[collection]:
            assert f"`{item}`" in text, f"{collection}:{item}"
