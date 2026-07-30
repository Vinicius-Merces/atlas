from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED = {
    "handoff_id","task_id","from_runtime","to_runtime",
    "checkpoint","context_pack","completed_steps","pending_steps",
    "validation","reviews","assumptions","remaining_risks"
}

def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_handoff.py <handoff.json>")
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = sorted(REQUIRED - data.keys())
    if missing:
        raise SystemExit(f"Missing fields: {', '.join(missing)}")
    if data["from_runtime"] == data["to_runtime"]:
        raise SystemExit("Source and target runtimes must differ")
    print(
        f"Valid handoff: {data['task_id']} "
        f"{data['from_runtime']} -> {data['to_runtime']}"
    )

if __name__ == "__main__":
    main()
