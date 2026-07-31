from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


EXCLUDED_ROOTS = {".git", ".atlas", ".vscode", "dist", "reports"}
EXCLUDED_PARTS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}
EXCLUDED_ROOT_FILES = {
    "APPLY-PATCH.md",
    "PATCH-MANIFEST.json",
    "FILES-TO-ADD.md",
    "FILES-TO-REPLACE.md",
    "FILES-TO-DELETE.md",
    "RECOVERY-MANIFEST.json",
    "README-RECOVERY.md",
}
SECRET_NAMES = {".env", "id_rsa", "id_ed25519"}
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_release_bytes(data: bytes) -> bytes:
    """Normalize UTF-8 text so archives are identical across checkout OSes."""
    if b"\0" in data:
        return data
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def is_release_path(relative: PurePosixPath) -> bool:
    if not relative.parts:
        return False
    if relative.parts[0] in EXCLUDED_ROOTS:
        return False
    if len(relative.parts) == 1 and relative.name in EXCLUDED_ROOT_FILES:
        return False
    if set(relative.parts) & EXCLUDED_PARTS:
        return False
    if relative.suffix.lower() in {".pyc", ".pyo", ".pem", ".key"}:
        return False
    if relative.name in SECRET_NAMES:
        return False
    return True


def source_payload(root: Path) -> dict[str, bytes]:
    payload: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = PurePosixPath(path.relative_to(root).as_posix())
        if is_release_path(relative):
            payload[relative.as_posix()] = canonical_release_bytes(
                path.read_bytes()
            )
    return payload


def content_manifest(payload: dict[str, bytes]) -> bytes:
    data = {
        "algorithm": "sha256",
        "files": [
            {
                "path": path,
                "sha256": sha256_bytes(content),
                "size": len(content),
            }
            for path, content in sorted(payload.items())
        ],
    }
    return (json.dumps(data, indent=2) + "\n").encode("utf-8")


def write_deterministic_zip(
    archive_path: Path, root_name: str, payload: dict[str, bytes]
) -> bytes:
    manifest = content_manifest(payload)
    archive_payload = dict(payload)
    archive_payload["CONTENT-MANIFEST.json"] = manifest

    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(
        archive_path,
        "w",
        compression=ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for relative, content in sorted(archive_payload.items()):
            name = f"{root_name}/{relative}"
            info = ZipInfo(name, date_time=FIXED_TIMESTAMP)
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content, compress_type=ZIP_DEFLATED, compresslevel=9)
    return manifest


def write_external_metadata(
    archive_path: Path,
    package_type: str,
    version: str,
    manifest_bytes: bytes,
    file_count: int,
    *,
    from_version: str | None = None,
) -> tuple[Path, Path]:
    archive_hash = sha256_file(archive_path)
    metadata = {
        "package_type": package_type,
        "version": version,
        "from_version": from_version,
        "to_version": version,
        "artifact": archive_path.name,
        "sha256": archive_hash,
        "content_manifest_sha256": sha256_bytes(manifest_bytes),
        "file_count": file_count,
    }
    manifest_path = archive_path.with_suffix(".manifest.json")
    checksum_path = archive_path.with_suffix(".sha256")
    manifest_path.write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    checksum_path.write_text(
        f"{archive_hash}  {archive_path.name}\n", encoding="utf-8"
    )
    return manifest_path, checksum_path
