from __future__ import annotations

from pathlib import Path

from scripts import build_project_brief, build_resume_packet


def test_resume_packet_excludes_generated_distribution_trees(
    tmp_path: Path,
    monkeypatch,
) -> None:
    canonical = tmp_path / ".claude" / "memory" / "architecture.md"
    generated = tmp_path / "dist" / "install" / ".claude" / "memory" / "architecture.md"
    canonical.parent.mkdir(parents=True)
    generated.parent.mkdir(parents=True)
    canonical.write_text("# Canonical\n", encoding="utf-8")
    generated.write_text("# Generated copy\n", encoding="utf-8")
    monkeypatch.setattr(build_resume_packet, "ROOT", tmp_path)

    assert build_resume_packet.existing(".claude/memory/*.md") == [
        ".claude/memory/architecture.md"
    ]


def test_project_brief_excludes_generated_distribution_adrs(
    tmp_path: Path,
    monkeypatch,
) -> None:
    canonical = tmp_path / "framework" / "adr" / "ADR-001-canonical.md"
    generated = tmp_path / "dist" / "install" / "framework" / "adr" / "ADR-999-copy.md"
    canonical.parent.mkdir(parents=True)
    generated.parent.mkdir(parents=True)
    canonical.write_text("# Canonical\n", encoding="utf-8")
    generated.write_text("# Generated copy\n", encoding="utf-8")
    monkeypatch.setattr(build_project_brief, "ROOT", tmp_path)

    paths = [
        path.relative_to(tmp_path).as_posix()
        for path in build_project_brief.project_paths("ADR-*.md")
    ]

    assert paths == ["framework/adr/ADR-001-canonical.md"]
