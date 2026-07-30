from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CODEX = ROOT / "adapters" / "codex"


def test_core_codex_roles_exist() -> None:
    required = [
        "agents/orchestrator.md",
        "agents/software-engineer.md",
        "agents/quality-reviewer.md",
    ]
    for relative in required:
        assert (CODEX / relative).is_file(), relative


def test_core_codex_commands_exist() -> None:
    required = [
        "commands/atlas-plan.md",
        "commands/atlas-review.md",
        "commands/atlas-implement.md",
        "commands/atlas-release.md",
    ]
    for relative in required:
        assert (CODEX / relative).is_file(), relative


def test_core_codex_workflows_exist() -> None:
    required = [
        "workflows/feature-delivery.md",
        "workflows/bug-fix.md",
        "workflows/release.md",
    ]
    for relative in required:
        assert (CODEX / relative).is_file(), relative
