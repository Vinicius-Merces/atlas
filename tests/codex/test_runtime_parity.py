from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_capability_matrix_declares_supported_parity() -> None:
    text = (
        ROOT / "compatibility" / "claude-codex-capability-matrix.md"
    ).read_text(encoding="utf-8")
    assert "supported" in text
    assert "Claude Code" in text
    assert "Codex" in text


def test_codex_uses_shared_contracts_and_memory() -> None:
    text = (
        ROOT / "adapters" / "codex" / "runtime-map.yaml"
    ).read_text(encoding="utf-8")
    assert "../../.claude/contracts/" in text
    assert "../../.claude/memory/" in text
