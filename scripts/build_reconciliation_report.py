from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    changed_files = []
    validation = []
    reviews = []
    risks = []

    for ws in manifest.get("workstreams", []):
        changed_files.extend(ws.get("changed_files", []))
        validation.extend(ws.get("validation", []))
        reviews.extend(ws.get("reviews", []))
        risks.extend(ws.get("remaining_risks", []))

    report = {
        "task_id": manifest["task_id"],
        "workstreams": [ws["workstream_id"] for ws in manifest.get("workstreams", [])],
        "changed_files": sorted(set(changed_files)),
        "combined_validation": sorted(set(validation)),
        "combined_reviews": sorted(set(reviews)),
        "conflicts": manifest.get("conflicts", []),
        "remaining_risks": sorted(set(risks)),
        "outcome": "ready" if not manifest.get("conflicts") else "blocked",
    }

    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(output)
    else:
        print(rendered, end="")

if __name__ == "__main__":
    main()
