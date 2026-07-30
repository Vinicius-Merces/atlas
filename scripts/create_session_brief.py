from __future__ import annotations
import argparse, json, uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True)
    parser.add_argument("--runtime", default="unknown")
    parser.add_argument("--next-action", default="Review repository state and continue pending work.")
    parser.add_argument("--output")
    args = parser.parse_args()

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    brief = {
        "session_id": f"session-{uuid.uuid4().hex[:12]}",
        "framework_version": version,
        "runtime": args.runtime,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "summary": args.summary,
        "completed_work": [],
        "changed_files": [],
        "validation": [],
        "decisions": [],
        "pending_work": [],
        "risks": [],
        "next_action": args.next_action,
    }

    output = Path(args.output) if args.output else (
        ROOT / ".atlas" / "continuity" / "latest-session.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(brief, indent=2) + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
