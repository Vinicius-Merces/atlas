from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_required_paths_exist() -> None:
    required = [
        "README.md",
        "VERSION",
        "CHANGELOG.md",
        "LICENSE",
        ".claude/registry.json",
        ".claude/runtime.yaml",
        "framework",
        "docs",
        "templates",
        "blueprints",
        "adapters",
        "scripts",
    ]
    for relative in required:
        assert (ROOT / relative).exists(), relative
