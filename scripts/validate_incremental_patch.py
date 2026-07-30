from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: validate_incremental_patch.py <installed-root> <patch-root>"
        )
    installed = Path(sys.argv[1])
    patch = Path(sys.argv[2])
    manifest = json.loads((patch / "PATCH-MANIFEST.json").read_text(encoding="utf-8"))

    installed_version = (installed / "VERSION").read_text(encoding="utf-8").strip()
    if installed_version != manifest["from_version"]:
        raise SystemExit(
            f"Expected base {manifest['from_version']}, found {installed_version}"
        )

    for item in manifest["files"]:
        path = patch / item["path"]
        if not path.is_file():
            raise SystemExit(f"Missing patch file: {item['path']}")
        if sha256(path) != item["sha256"]:
            raise SystemExit(f"Hash mismatch: {item['path']}")

    print(
        f"Patch valid: {manifest['from_version']} -> {manifest['to_version']} "
        f"({len(manifest['files'])} files)"
    )

if __name__ == "__main__":
    main()
