from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_claude_bootstrap_imports_shared_atlas_instructions() -> None:
    bootstrap = read("CLAUDE.md")

    assert "@AGENTS.md" in bootstrap
    assert ".atlas/continuity/resume-packet.json" in bootstrap
    assert ".claude/commands/" in bootstrap
    assert ".claude/skills/*/SKILL.md" in bootstrap
    assert "Markdown workflows" in bootstrap
    assert "execution evidence" in bootstrap


def test_stable_runtime_support_surfaces_are_consistent() -> None:
    version = read("VERSION").strip()
    registry = json.loads(read(".claude/registry.json"))
    support = registry["runtime_support"]

    assert "-" not in version
    assert "beta" not in registry
    assert support["release_channel"] == "stable"
    assert support["status"] == "supported"
    assert support["canonical_runtime"] == "claude-code"
    assert support["supported_runtimes"] == ["claude-code", "codex"]

    codex_readme = read("adapters/codex/README.md")
    systems = read("obsidian/atlas/Systems.md")
    assert "**Support:** Supported compatibility runtime" in codex_readme
    assert "Beta-supported compatibility runtime" not in codex_readme
    assert "Codex: supported compatibility adapter" in systems
    assert "Codex: beta-supported adapter" not in systems


def test_runtime_documentation_describes_interpreted_procedures() -> None:
    matrix = read("compatibility/claude-codex-capability-matrix.md")
    bootstrap_guide = read("docs/claude-code-bootstrap-guide.md")
    index = read("docs/INDEX.md")

    assert "Native workflow files" not in matrix
    assert "Native `.claude/skills/*/SKILL.md` prompts" in matrix
    assert "Runtime-native, semantic" in matrix
    assert "`.claude/command`" not in bootstrap_guide
    assert "`.claude/commands/`" in bootstrap_guide
    assert "[Daily Quickstart](daily-quickstart.md)" in index
