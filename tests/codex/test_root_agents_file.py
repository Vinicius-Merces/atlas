from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_root_agents_file_exists() -> None:
    assert (ROOT / "AGENTS.md").is_file()


def test_root_agents_file_points_to_shared_memory() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert ".claude/memory/" in text
    assert ".claude/contracts/" in text
    assert "adapters/codex/" in text
