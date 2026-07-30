from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    DIST.mkdir(exist_ok=True)

    archive_path = DIST / f"atlas-framework-{version}.zip"
    excluded_roots = {".git", "dist"}

    with ZipFile(archive_path, "w", ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT)
            if relative.parts and relative.parts[0] in excluded_roots:
                continue
            archive.write(path, Path(f"atlas-framework-{version}") / relative)

    manifest = {
        "version": version,
        "artifact": archive_path.name,
        "sha256": sha256(archive_path),
    }

    manifest_path = DIST / f"atlas-framework-{version}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"Created {archive_path}")
    print(f"Created {manifest_path}")


if __name__ == "__main__":
    main()
