from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--to-runtime", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    checkpoint_path = Path(args.checkpoint)
    checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    handoff = {
        "handoff_id": f"handoff-{uuid.uuid4().hex[:12]}",
        "task_id": checkpoint["task_id"],
        "from_runtime": checkpoint["runtime"],
        "to_runtime": args.to_runtime,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "checkpoint": str(checkpoint_path),
        "context_pack": checkpoint.get("context_pack", ""),
        "completed_steps": checkpoint["completed_steps"],
        "pending_steps": checkpoint["pending_steps"],
        "changed_files": checkpoint["changed_files"],
        "validation": checkpoint["validation"],
        "reviews": checkpoint["reviews"],
        "assumptions": checkpoint["assumptions"],
        "remaining_risks": checkpoint["remaining_risks"],
    }
    output = Path(args.output) if args.output else Path(
        f"{handoff['handoff_id']}.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(handoff, indent=2) + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
