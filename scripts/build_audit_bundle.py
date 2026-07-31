from __future__ import annotations
import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

from release_utils import canonical_release_bytes, sha256_bytes

ROOT = Path(__file__).resolve().parents[1]

def sha256(path: Path) -> str:
    return sha256_bytes(canonical_release_bytes(path.read_bytes()))

def collect(workspace: Path, directory: str) -> list[dict]:
    requested = Path(directory)
    if requested.is_absolute():
        raise ValueError(f"Audit include must be workspace-relative: {directory}")
    root = (workspace / requested).resolve()
    if not root.is_relative_to(workspace):
        raise ValueError(f"Audit include escapes workspace: {directory}")
    if not root.exists():
        return []
    return [
        {
            "path": path.relative_to(workspace).as_posix(),
            "sha256": sha256(path),
        }
        for path in sorted(root.rglob("*.json"))
        if path.is_file()
    ]

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--output")
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help=(
            "Additional workspace-relative JSON record directory. "
            "May be supplied more than once."
        ),
    )
    parser.add_argument(
        "--no-default-includes",
        action="store_true",
        help="Collect only directories supplied with --include.",
    )
    args = parser.parse_args()

    workspace = Path(args.root).resolve()
    version = (workspace / "VERSION").read_text(encoding="utf-8").strip()
    records = []
    directories = [] if args.no_default_includes else [
        ".atlas/evidence",
        ".atlas/deployments",
        ".atlas/continuity",
    ]
    directories.extend(args.include)
    for directory in dict.fromkeys(directories):
        records.extend(collect(workspace, directory))

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

    output = (
        Path(args.output)
        if args.output
        else workspace / ".atlas" / "audit" / "audit-bundle.json"
    )
    if not output.is_absolute():
        output = workspace / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(output)

if __name__ == "__main__":
    main()
