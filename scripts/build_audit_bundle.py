from __future__ import annotations
import hashlib, json, uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def collect(directory: str) -> list[dict]:
    root = ROOT / directory
    if not root.exists():
        return []
    return [
        {
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256(path),
        }
        for path in sorted(root.rglob("*.json"))
        if path.is_file()
    ]

def main() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    records = []
    for directory in [
        ".atlas/evidence",
        ".atlas/deployments",
        ".atlas/continuity",
    ]:
        records.extend(collect(directory))

    manifest = {
        "bundle_id": f"audit-{uuid.uuid4().hex[:12]}",
        "framework_version": version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "repository",
        "records": records,
        "integrity": {
            "algorithm": "sha256",
            "record_count": len(records),
        },
    }

    output = ROOT / ".atlas" / "audit" / "audit-bundle.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
