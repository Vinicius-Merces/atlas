from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    failures = []
    for ws in manifest.get("workstreams", []):
        if ws.get("status") not in {"completed", "validated"}:
            failures.append(f"{ws['workstream_id']} is {ws.get('status')}")
        if not ws.get("validation"):
            failures.append(f"{ws['workstream_id']} has no validation evidence")

    if failures:
        print("Merge readiness failed:")
        for item in failures:
            print(f"- {item}")
        raise SystemExit(1)

    print(f"Merge ready: {manifest['task_id']}")

if __name__ == "__main__":
    main()
