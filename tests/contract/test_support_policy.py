from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_support_policy_declares_canonical_runtime() -> None:
    text = (ROOT / "compatibility" / "support-policy.md").read_text(encoding="utf-8")
    assert "Claude Code" in text
    assert "canonical beta-supported runtime" in text


def test_experimental_adapters_are_visible() -> None:
    text = (ROOT / "compatibility" / "support-policy.md").read_text(encoding="utf-8")
    for runtime in ["Codex", "Gemini", "Cursor"]:
        assert runtime in text
