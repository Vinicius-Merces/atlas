from __future__ import annotations

import argparse
import json
from fnmatch import fnmatchcase
from pathlib import Path

if __package__:
    from .project_memory_utils import framework_version, identity
else:
    from project_memory_utils import framework_version, identity

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_ADR_ROOTS = ("framework/adr",)


def project_paths(pattern: str) -> list[Path]:
    paths = []
    for relative_root in CANONICAL_ADR_ROOTS:
        canonical_root = ROOT / relative_root
        if not canonical_root.is_dir():
            continue
        paths.extend(
            path
            for path in canonical_root.rglob("*")
            if path.is_file() and fnmatchcase(path.name, pattern)
        )
    return sorted(paths)


def read_optional(relative: str, limit: int = 6000) -> str:
    path = ROOT / relative
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")[:limit].strip()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Build the repository-native ATLAS project brief."
    )
    parser.parse_args(argv)

    version = framework_version(ROOT)
    brief = {
        "framework_version": version,
        "project_name": ROOT.name,
        "purpose": read_optional("README.md", 1200),
        "architecture": read_optional(".claude/memory/architecture.md"),
        "current_state": read_optional("CHANGELOG.md", 3000),
        "active_work": [],
        "decisions": sorted(
            path.relative_to(ROOT).as_posix()
            for path in project_paths("ADR-*.md")
        )[-20:],
        "risks": [],
        "next_actions": [
            "Review the latest session brief.",
            "Validate memory freshness.",
            "Inspect current repository status.",
        ],
        "sources": [
            "README.md",
            "CHANGELOG.md",
            ".claude/memory/",
            "docs/",
            "framework/",
        ],
    }
    if identity(ROOT):
        brief["project_id"] = identity(ROOT)["project_id"]
        brief["project_name"] = identity(ROOT)["project_name"]
        brief["sources"] = [name for name in brief["sources"] if (ROOT / name).exists()]

    output = ROOT / ".atlas" / "continuity" / "project-brief.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(brief, indent=2) + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
