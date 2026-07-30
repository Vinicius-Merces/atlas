from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / ".atlas" / "audit" / "audit-bundle.json"

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main() -> None:
    if not BUNDLE.is_file():
        raise SystemExit("Run scripts/build_audit_bundle.py first")

    bundle = json.loads(BUNDLE.read_text(encoding="utf-8"))
    failures = []

    for record in bundle["records"]:
        path = ROOT / record["path"]
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
