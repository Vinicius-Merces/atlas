from __future__ import annotations
import argparse, json, uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--runtime", required=True)
    parser.add_argument("--status", default="in-progress")
    parser.add_argument("--output")
    args = parser.parse_args()

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    record = {
        "evidence_id": f"evidence-{uuid.uuid4().hex[:12]}",
        "task_id": args.task_id,
        "framework_version": version,
        "runtime": args.runtime,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sources": [],
        "decisions": [],
        "changed_files": [],
        "validation": [],
        "reviews": [],
        "assumptions": [],
        "remaining_risks": [],
        "status": args.status,
    }

    output = Path(args.output) if args.output else (
        ROOT / ".atlas" / "evidence" / f"{record['evidence_id']}.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
