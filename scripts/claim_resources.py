from __future__ import annotations
import argparse, json, uuid
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workstream", required=True)
    parser.add_argument("--mode", choices=["shared", "exclusive"], default="exclusive")
    parser.add_argument("--resource", action="append", required=True)
    parser.add_argument("--reason", default="planned implementation")
    parser.add_argument("--output")
    args = parser.parse_args()

    workstream = json.loads(Path(args.workstream).read_text(encoding="utf-8"))
    claim = {
        "claim_id": f"claim-{uuid.uuid4().hex[:10]}",
        "workstream_id": workstream["workstream_id"],
        "mode": args.mode,
        "resources": sorted(set(args.resource)),
        "reason": args.reason,
    }
    rendered = json.dumps(claim, indent=2) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(output)
    else:
        print(rendered, end="")

if __name__ == "__main__":
    main()
