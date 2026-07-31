from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTINUITY = ROOT / ".atlas" / "continuity"

def existing(pattern: str) -> list[str]:
    return sorted(
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob(pattern)
        if path.is_file()
    )

def main() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    project_brief = CONTINUITY / "project-brief.json"
    latest_session = CONTINUITY / "latest-session.json"

    packet = {
        "framework_version": version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_brief": project_brief.relative_to(ROOT).as_posix() if project_brief.exists() else "",
        "latest_session": latest_session.relative_to(ROOT).as_posix() if latest_session.exists() else "",
        "memory_sources": existing(".claude/memory/*.md"),
        "open_tasks": existing("*.task.json"),
        "checkpoints": existing("checkpoint-*.json"),
        "handoffs": existing("handoff-*.json"),
        "workstreams": existing("ws-*.json"),
        "risks": [],
        "next_actions": [
            "Read AGENTS.md.",
            "Read the project brief and latest session.",
            "Validate memory freshness.",
            "Inspect Git status and pending task artifacts.",
        ],
    }

    output = CONTINUITY / "resume-packet.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
