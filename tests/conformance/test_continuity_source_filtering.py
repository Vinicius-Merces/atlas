from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import build_project_brief, build_resume_packet
from scripts import validate_source_of_truth


def test_resume_packet_reads_memory_only_from_the_canonical_root(
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

    assert build_resume_packet.existing(
        build_resume_packet.MEMORY_ROOT,
        "*.md",
    ) == [
        ".claude/memory/architecture.md"
    ]


def test_project_brief_reads_only_case_sensitive_canonical_adrs(
    tmp_path: Path,
    monkeypatch,
) -> None:
    canonical = tmp_path / "framework" / "adr" / "ADR-001-canonical.md"
    lowercase = tmp_path / "framework" / "adr" / "adr-draft.md"
    generated = tmp_path / "dist" / "install" / "framework" / "adr" / "ADR-999-copy.md"
    example = tmp_path / "examples" / "adr" / "ADR-002-example.md"
    skill = tmp_path / ".claude" / "skills" / "architecture" / "adr-authoring.md"
    template = tmp_path / "templates" / "adr-template.md"
    canonical.parent.mkdir(parents=True)
    generated.parent.mkdir(parents=True)
    example.parent.mkdir(parents=True)
    skill.parent.mkdir(parents=True)
    template.parent.mkdir(parents=True)
    canonical.write_text("# Canonical\n", encoding="utf-8")
    lowercase.write_text("# Draft\n", encoding="utf-8")
    generated.write_text("# Generated copy\n", encoding="utf-8")
    example.write_text("# Example\n", encoding="utf-8")
    skill.write_text("# Skill\n", encoding="utf-8")
    template.write_text("# Template\n", encoding="utf-8")
    monkeypatch.setattr(build_project_brief, "ROOT", tmp_path)

    paths = [
        path.relative_to(tmp_path).as_posix()
        for path in build_project_brief.project_paths("ADR-*.md")
    ]

    assert paths == ["framework/adr/ADR-001-canonical.md"]


def test_resume_packet_reads_execution_artifacts_only_from_continuity_root(
    tmp_path: Path,
    monkeypatch,
) -> None:
    continuity = tmp_path / ".atlas" / "continuity"
    schemas = tmp_path / "schemas"
    templates = tmp_path / "templates"
    continuity.mkdir(parents=True)
    schemas.mkdir()
    templates.mkdir()

    expected = {
        "task": continuity / "feature.task.json",
        "checkpoint": continuity / "checkpoint-live.json",
        "handoff": continuity / "handoff-live.json",
        "workstream": continuity / "ws-live.json",
    }
    false_positives = [
        schemas / "handoff-manifest.json",
        templates / "handoff-example.json",
        templates / "checkpoint-example.json",
        templates / "ws-example.json",
        templates / "example.task.json",
        continuity / "HANDOFF-draft.json",
    ]
    for path in [*expected.values(), *false_positives]:
        path.write_text("{}\n", encoding="utf-8")

    (tmp_path / "VERSION").write_text("0.1.0\n", encoding="utf-8")
    monkeypatch.setattr(build_resume_packet, "ROOT", tmp_path)

    assert build_resume_packet.existing(
        build_resume_packet.CONTINUITY_ROOT,
        "*.task.json",
    ) == [".atlas/continuity/feature.task.json"]
    assert build_resume_packet.existing(
        build_resume_packet.CONTINUITY_ROOT,
        "checkpoint-*.json",
    ) == [".atlas/continuity/checkpoint-live.json"]
    assert build_resume_packet.existing(
        build_resume_packet.CONTINUITY_ROOT,
        "handoff-*.json",
    ) == [".atlas/continuity/handoff-live.json"]
    assert build_resume_packet.existing(
        build_resume_packet.CONTINUITY_ROOT,
        "ws-*.json",
    ) == [".atlas/continuity/ws-live.json"]

    build_resume_packet.main([])
    packet = json.loads(
        (continuity / "resume-packet.json").read_text(encoding="utf-8")
    )
    assert packet["open_tasks"] == [".atlas/continuity/feature.task.json"]
    assert packet["checkpoints"] == [".atlas/continuity/checkpoint-live.json"]
    assert packet["handoffs"] == [".atlas/continuity/handoff-live.json"]
    assert packet["workstreams"] == [".atlas/continuity/ws-live.json"]


def test_source_of_truth_rejects_fallback_for_missing_canonical_source(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    manifest = tmp_path / "source-of-truth-manifest.json"
    (tmp_path / "VERSION").write_text("0.1.0\n", encoding="utf-8")
    fallback = tmp_path / "examples" / "adr"
    fallback.mkdir(parents=True)
    manifest.write_text(
        json.dumps(
            {
                "framework_version": "0.1.0",
                "domains": {
                    "architecture_decisions": {
                        "source": "framework/adr/",
                        "type": "directory",
                        "fallbacks": ["examples/adr/"],
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(validate_source_of_truth, "ROOT", tmp_path)
    monkeypatch.setattr(validate_source_of_truth, "MANIFEST", manifest)

    with pytest.raises(SystemExit) as error:
        validate_source_of_truth.main()

    assert error.value.code == 1
    assert (
        "Missing source for architecture_decisions: framework/adr/"
        in capsys.readouterr().out
    )


def test_architecture_decisions_manifest_uses_framework_adr() -> None:
    root = Path(__file__).resolve().parents[2]
    manifest = json.loads(
        (
            root / "adapters" / "shared" / "source-of-truth-manifest.json"
        ).read_text(encoding="utf-8")
    )

    assert manifest["domains"]["architecture_decisions"] == {
        "source": "framework/adr/",
        "type": "directory",
    }
