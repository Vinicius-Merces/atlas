from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-envelope", required=True)
    parser.add_argument("--runtime", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    envelope = json.loads(Path(args.task_envelope).read_text(encoding="utf-8"))
    checkpoint = {
        "checkpoint_id": f"checkpoint-{uuid.uuid4().hex[:12]}",
        "task_id": envelope["id"],
        "runtime": args.runtime,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "state": envelope.get("state", "executing"),
        "completed_steps": [],
        "pending_steps": ["continue-routed-workflow"],
        "changed_files": [],
        "validation": [],
        "reviews": [],
        "assumptions": [],
        "remaining_risks": [],
        "context_pack": envelope.get("context_pack", ""),
    }
    output = Path(args.output) if args.output else Path(
        f"{checkpoint['checkpoint_id']}.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(checkpoint, indent=2) + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
