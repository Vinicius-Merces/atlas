import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_deprecation_registry_version_matches() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    data = json.loads((ROOT / "compatibility" / "deprecations.json").read_text(encoding="utf-8"))
    assert data["version"] == version


def test_runtime_matrix_exists() -> None:
    text = (ROOT / "compatibility" / "runtime-matrix.md").read_text(encoding="utf-8")
    assert "Claude Code" in text
    assert "Codex" in text
