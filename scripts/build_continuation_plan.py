from __future__ import annotations

import argparse
import json
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    handoff_path = Path(args.handoff)
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    plan = {
        "task_id": handoff["task_id"],
        "runtime": handoff["to_runtime"],
        "handoff": str(handoff_path),
        "preserved_steps": handoff["completed_steps"],
        "next_steps": handoff["pending_steps"],
        "required_validation": handoff["validation"],
        "required_reviews": handoff["reviews"],
        "assumptions": handoff["assumptions"],
        "remaining_risks": handoff["remaining_risks"],
        "instructions": [
            "validate-handoff",
            "load-checkpoint",
            "load-context-pack",
            "verify-changed-files",
            "resume-pending-steps",
            "rerun-required-validation",
            "complete-required-reviews",
            "produce-execution-result",
        ],
    }
    rendered = json.dumps(plan, indent=2) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(output)
    else:
        print(rendered, end="")

if __name__ == "__main__":
    main()
