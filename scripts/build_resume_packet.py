from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from fnmatch import fnmatchcase
from pathlib import Path

if __package__:
    from .project_memory_utils import framework_version, identity
else:
    from project_memory_utils import framework_version, identity

ROOT = Path(__file__).resolve().parents[1]
CONTINUITY_ROOT = ".atlas/continuity"
MEMORY_ROOT = ".claude/memory"


def existing(relative_root: str, pattern: str) -> list[str]:
    root = ROOT / relative_root
    if not root.is_dir():
        return []
    return sorted(
        path.relative_to(ROOT).as_posix()
        for path in root.rglob("*")
        if path.is_file() and fnmatchcase(path.name, pattern)
    )


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Build the repository-native ATLAS resume packet."
    )
    parser.parse_args(argv)

    version = framework_version(ROOT)
    continuity = ROOT / CONTINUITY_ROOT
    project_brief = continuity / "project-brief.json"
    latest_session = continuity / "latest-session.json"
    session = json.loads(latest_session.read_text(encoding="utf-8")) if latest_session.exists() else {}

    packet = {
        "framework_version": version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_brief": project_brief.relative_to(ROOT).as_posix() if project_brief.exists() else "",
        "latest_session": latest_session.relative_to(ROOT).as_posix() if latest_session.exists() else "",
        "memory_sources": existing(MEMORY_ROOT, "*.md"),
        "open_tasks": existing(CONTINUITY_ROOT, "*.task.json"),
        "checkpoints": existing(CONTINUITY_ROOT, "checkpoint-*.json"),
        "handoffs": existing(CONTINUITY_ROOT, "handoff-*.json"),
        "workstreams": existing(CONTINUITY_ROOT, "ws-*.json"),
        "risks": session.get("risks", []),
        "next_actions": [
            "Read AGENTS.md.",
            "Read the project brief and latest session.",
            "Validate memory freshness.",
            "Inspect Git status and pending task artifacts.",
            *([session["next_action"]] if session.get("next_action") else []),
            *session.get("pending_work", []),
        ],
    }

    if identity(ROOT):
        packet["project_id"] = identity(ROOT)["project_id"]

    output = continuity / "resume-packet.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
