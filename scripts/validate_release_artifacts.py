from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

from release_utils import (
    EXCLUDED_PARTS,
    FIXED_TIMESTAMP,
    SECRET_NAMES,
    sha256_bytes,
    sha256_file,
)


INCREMENTAL_METADATA = {
    "APPLY-PATCH.md",
    "PATCH-MANIFEST.json",
    "FILES-TO-ADD.md",
    "FILES-TO-REPLACE.md",
    "FILES-TO-DELETE.md",
}


def safe_path(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts


def markdown_paths(content: bytes) -> set[str]:
    return set(re.findall(r"- `([^`]+)`", content.decode("utf-8")))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", required=True)
    parser.add_argument("--manifest")
    parser.add_argument("--checksum")
    args = parser.parse_args()

    archive_path = Path(args.archive).resolve()
    manifest_path = (
        Path(args.manifest).resolve()
        if args.manifest
        else archive_path.with_suffix(".manifest.json")
    )
    checksum_path = (
        Path(args.checksum).resolve()
        if args.checksum
        else archive_path.with_suffix(".sha256")
    )
    failures: list[str] = []

    external = json.loads(manifest_path.read_text(encoding="utf-8"))
    archive_hash = sha256_file(archive_path)
    if external.get("artifact") != archive_path.name:
        failures.append("External manifest artifact name mismatch")
    if external.get("sha256") != archive_hash:
        failures.append("External manifest archive hash mismatch")
    checksum_parts = checksum_path.read_text(encoding="utf-8").strip().split()
    if checksum_parts != [archive_hash, archive_path.name]:
        failures.append("External checksum file mismatch")

    with ZipFile(archive_path) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos if not info.is_dir()]
        if len(names) != len(set(names)):
            failures.append("Archive contains duplicate paths")
        for info in infos:
            if info.date_time != FIXED_TIMESTAMP:
                failures.append(f"Non-deterministic timestamp: {info.filename}")
            if not safe_path(info.filename):
                failures.append(f"Unsafe archive path: {info.filename}")

        roots = {PurePosixPath(name).parts[0] for name in names}
        if len(roots) != 1:
            failures.append("Archive must contain exactly one versioned root")
            root_name = ""
        else:
            root_name = next(iter(roots))
        contents = {
            PurePosixPath(name).relative_to(root_name).as_posix(): archive.read(name)
            for name in names
            if root_name
        }

    for relative in contents:
        parts = set(PurePosixPath(relative).parts)
        if parts & EXCLUDED_PARTS:
            failures.append(f"Forbidden cache path: {relative}")
        name = PurePosixPath(relative).name
        suffix = PurePosixPath(relative).suffix.lower()
        if name in SECRET_NAMES or suffix in {".pem", ".key", ".pyc", ".pyo"}:
            failures.append(f"Forbidden secret or generated file: {relative}")

    manifest_bytes = contents.get("CONTENT-MANIFEST.json")
    if manifest_bytes is None:
        failures.append("Internal CONTENT-MANIFEST.json is missing")
        content_entries = {}
    else:
        if external.get("content_manifest_sha256") != sha256_bytes(manifest_bytes):
            failures.append("Internal content manifest hash mismatch")
        content_manifest = json.loads(manifest_bytes.decode("utf-8"))
        entries = content_manifest.get("files", [])
        content_entries = {entry["path"]: entry for entry in entries}
        expected = set(contents) - {"CONTENT-MANIFEST.json"}
        if set(content_entries) != expected or len(entries) != len(expected):
            failures.append("Internal content manifest path set mismatch")
        for relative in expected & set(content_entries):
            entry = content_entries[relative]
            content = contents[relative]
            if entry.get("sha256") != sha256_bytes(content):
                failures.append(f"Content hash mismatch: {relative}")
            if entry.get("size") != len(content):
                failures.append(f"Content size mismatch: {relative}")
        if external.get("file_count") != len(expected):
            failures.append("External file count mismatch")

    package_type = external.get("package_type")
    version = external.get("version")
    if version and version not in root_name:
        failures.append("Versioned archive root does not match external manifest")

    if package_type in {"cumulative", "recovery"}:
        required = {
            "VERSION",
            "README.md",
            "CHANGELOG.md",
            "LICENSE",
            ".claude/registry.json",
        }
        missing = required - contents.keys()
        if missing:
            failures.append(
                f"Cumulative package missing: {', '.join(sorted(missing))}"
            )
        if "VERSION" in contents:
            internal_version = contents["VERSION"].decode("utf-8").strip()
            if internal_version != version:
                failures.append("Packaged VERSION mismatch")
        if not any(path.startswith(".claude/") for path in contents):
            failures.append("Cumulative package has no canonical .claude payload")
        for forbidden_root in [".atlas/", ".vscode/", "reports/", "dist/"]:
            if any(path.startswith(forbidden_root) for path in contents):
                failures.append(f"Cumulative package includes {forbidden_root}")
        if package_type == "recovery" and "RECOVERY-INSTRUCTIONS.md" not in contents:
            failures.append("Recovery instructions are missing")

    elif package_type == "incremental":
        missing = INCREMENTAL_METADATA - contents.keys()
        if missing:
            failures.append(
                f"Incremental package missing: {', '.join(sorted(missing))}"
            )
        if not missing:
            patch = json.loads(contents["PATCH-MANIFEST.json"].decode("utf-8"))
            if patch.get("from_version") != external.get("from_version"):
                failures.append("Incremental base version mismatch")
            if patch.get("to_version") != version:
                failures.append("Incremental target version mismatch")

            declared_payloads = set()
            operations = {"add": set(), "replace": set(), "delete": set()}
            for item in patch.get("files", []):
                operation = item.get("operation")
                target = item.get("target_path", item.get("path", ""))
                packaged = item.get("package_path", "")
                if operation not in operations:
                    failures.append(f"Invalid operation: {operation}")
                    continue
                operations[operation].add(
                    target if operation == "delete" else packaged
                )
                if not safe_path(target):
                    failures.append(f"Unsafe target path: {target}")
                if operation == "delete":
                    if item.get("sha256"):
                        failures.append(f"Delete has payload hash: {target}")
                    continue
                if not safe_path(packaged):
                    failures.append(f"Unsafe package path: {packaged}")
                    continue
                declared_payloads.add(packaged)
                content = contents.get(packaged)
                if content is None:
                    failures.append(f"Missing incremental payload: {packaged}")
                elif item.get("sha256") != sha256_bytes(content):
                    failures.append(f"Incremental payload hash mismatch: {packaged}")
                if target.startswith(".claude/") and not packaged.startswith(
                    "CLAUDE-DIRECTORY/"
                ):
                    failures.append(f"Invalid .claude mapping: {packaged} -> {target}")
                if packaged.startswith("CLAUDE-DIRECTORY/") and not target.startswith(
                    ".claude/"
                ):
                    failures.append(f"Invalid visible mapping: {packaged} -> {target}")

            actual_payloads = (
                set(contents)
                - INCREMENTAL_METADATA
                - {"CONTENT-MANIFEST.json"}
            )
            if actual_payloads != declared_payloads:
                failures.append("Incremental archive has undeclared or missing payloads")
            if markdown_paths(contents["FILES-TO-ADD.md"]) != operations["add"]:
                failures.append("FILES-TO-ADD.md does not match manifest")
            if markdown_paths(contents["FILES-TO-REPLACE.md"]) != operations["replace"]:
                failures.append("FILES-TO-REPLACE.md does not match manifest")
            if markdown_paths(contents["FILES-TO-DELETE.md"]) != operations["delete"]:
                failures.append("FILES-TO-DELETE.md does not match manifest")
    else:
        failures.append(f"Unknown package type: {package_type}")

    if failures:
        print("Release artifact validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print(
        f"Release artifact valid: {package_type} {version} "
        f"({external['file_count']} payload files)"
    )


if __name__ == "__main__":
    main()
