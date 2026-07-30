from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-envelope", required=True)
    parser.add_argument("--runtime", choices=["claude", "codex"], required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    envelope = json.loads(Path(args.task_envelope).read_text(encoding="utf-8"))
    declaration = json.loads(
        (ROOT / "adapters" / args.runtime / "runtime-declaration.json")
        .read_text(encoding="utf-8")
    )

    plan = {
        "task_id": envelope["id"],
        "runtime": declaration["runtime"],
        "primary_role": envelope["primary_role"],
        "supporting_roles": envelope.get("supporting_roles", []),
        "workflow": envelope["workflow"],
        "skills": envelope.get("skills", []),
        "reviews": envelope["reviews"],
        "validation": envelope["validation"],
        "steps": [
            "validate-task-envelope",
            "load-context-pack",
            "load-runtime-declaration",
            "execute-workflow",
            "run-validation",
            "run-reviews",
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
