from __future__ import annotations
import argparse
import json
from pathlib import Path

from release_utils import canonical_release_bytes, sha256_bytes

ROOT = Path(__file__).resolve().parents[1]

def sha256(path: Path) -> str:
    return sha256_bytes(canonical_release_bytes(path.read_bytes()))

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--bundle")
    args = parser.parse_args()

    workspace = Path(args.root).resolve()
    bundle_path = (
        Path(args.bundle)
        if args.bundle
        else workspace / ".atlas" / "audit" / "audit-bundle.json"
    )
    if not bundle_path.is_absolute():
        bundle_path = workspace / bundle_path
    if not bundle_path.is_file():
        raise SystemExit("Run scripts/build_audit_bundle.py first")

    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    failures = []

    for record in bundle["records"]:
        path = (workspace / record["path"]).resolve()
        try:
            path.relative_to(workspace)
        except ValueError:
            failures.append(f"Path escapes workspace: {record['path']}")
            continue
        if not path.is_file():
            failures.append(f"Missing: {record['path']}")
        elif sha256(path) != record["sha256"]:
            failures.append(f"Hash mismatch: {record['path']}")

    if failures:
        print("Evidence integrity failed:")
        for item in failures:
            print(f"- {item}")
        raise SystemExit(1)

    print(f"Evidence integrity passed for {len(bundle['records'])} records.")

if __name__ == "__main__":
    main()
