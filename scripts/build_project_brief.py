from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_optional(relative: str, limit: int = 6000) -> str:
    path = ROOT / relative
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")[:limit].strip()

def main() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    brief = {
        "framework_version": version,
        "project_name": ROOT.name,
        "purpose": read_optional("README.md", 1200),
        "architecture": read_optional(".claude/memory/architecture.md"),
        "current_state": read_optional("CHANGELOG.md", 3000),
        "active_work": [],
        "decisions": sorted(
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("ADR-*.md")
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
    output = ROOT / ".atlas" / "continuity" / "project-brief.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(brief, indent=2) + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
