from __future__ import annotations

import argparse
import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "adapters" / "shared" / "task-routing-policy.json"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-type", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    route = next(
        (item for item in policy["routes"] if item["task_type"] == args.task_type),
        policy["fallback"],
    )

    envelope = {
        "id": f"task-{uuid.uuid4().hex[:12]}",
        "task_type": args.task_type,
        "summary": args.summary,
        "primary_role": route["primary_role"],
        "supporting_roles": route.get("supporting_roles", []),
        "workflow": route["workflow"],
        "skills": route.get("skills", []),
        "reviews": route.get("reviews", []),
        "validation": route.get("validation", ["project-appropriate-validation"]),
        "context_pack": "",
        "state": "routed",
    }

    rendered = json.dumps(envelope, indent=2) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(output)
    else:
        print(rendered, end="")

if __name__ == "__main__":
    main()
