from __future__ import annotations
import argparse, json, uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_list(path: Path) -> list[str]:
    if not path.is_file():
        return []
    items = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("- `") and line.endswith("`"):
            items.append(line[3:-1])
    return items

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-version", required=True)
    parser.add_argument("--to-version", required=True)
    parser.add_argument("--patch", default="")
    parser.add_argument("--patch-root")
    parser.add_argument("--status", default="applied")
    parser.add_argument("--output")
    args = parser.parse_args()

    patch_root = Path(args.patch_root) if args.patch_root else None
    receipt = {
        "receipt_id": f"deploy-{uuid.uuid4().hex[:12]}",
        "from_version": args.from_version,
        "to_version": args.to_version,
        "patch": args.patch,
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "files_added": read_list(patch_root / "FILES-TO-ADD.md") if patch_root else [],
        "files_replaced": read_list(patch_root / "FILES-TO-REPLACE.md") if patch_root else [],
        "files_deleted": read_list(patch_root / "FILES-TO-DELETE.md") if patch_root else [],
        "validation": [],
        "operator_notes": [],
        "status": args.status,
    }

    output = Path(args.output) if args.output else (
        ROOT / ".atlas" / "deployments" / f"{receipt['receipt_id']}.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
