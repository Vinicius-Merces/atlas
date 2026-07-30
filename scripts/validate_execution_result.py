from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED = {
    "task_id", "runtime", "status", "summary",
    "changed_files", "validation", "reviews",
    "assumptions", "remaining_risks"
}
ALLOWED_STATUS = {"completed", "partial", "blocked", "failed"}

def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_execution_result.py <execution-result.json>")
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = sorted(REQUIRED - data.keys())
    if missing:
        raise SystemExit(f"Missing required fields: {', '.join(missing)}")
    if data["status"] not in ALLOWED_STATUS:
        raise SystemExit(f"Invalid status: {data['status']}")
    print(f"Valid execution result: {data['task_id']} ({data['status']})")

if __name__ == "__main__":
    main()
