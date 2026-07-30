from __future__ import annotations
import argparse, json, uuid
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task-envelope", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    envelope = json.loads(Path(args.task_envelope).read_text(encoding="utf-8"))
    roles = [envelope["primary_role"], *envelope.get("supporting_roles", [])]
    roles = list(dict.fromkeys(roles)) or ["orchestrator"]

    workstreams = []
    for index, role in enumerate(roles, start=1):
        workstreams.append({
            "workstream_id": f"ws-{uuid.uuid4().hex[:10]}",
            "task_id": envelope["id"],
            "summary": f"{role} workstream for: {envelope['summary']}",
            "runtime": "unassigned",
            "owner_role": role,
            "dependencies": [],
            "resource_claims": [],
            "validation": envelope.get("validation", []),
            "reviews": envelope.get("reviews", []),
            "completion_criteria": ["workstream-output-validated"],
            "status": "planned",
        })

    manifest = {
        "task_id": envelope["id"],
        "workstreams": workstreams,
        "claims": [],
        "dependencies": [],
        "status": "planned",
    }
    rendered = json.dumps(manifest, indent=2) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(output)
    else:
        print(rendered, end="")

if __name__ == "__main__":
    main()
