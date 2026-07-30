from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED = {
    "id", "task_type", "summary", "primary_role",
    "workflow", "reviews", "validation"
}

def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_task_envelope.py <task-envelope.json>")
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = sorted(REQUIRED - data.keys())
    if missing:
        raise SystemExit(f"Missing required fields: {', '.join(missing)}")
    if not isinstance(data["reviews"], list) or not isinstance(data["validation"], list):
        raise SystemExit("reviews and validation must be arrays")
    print(f"Valid task envelope: {data['id']}")

if __name__ == "__main__":
    main()
