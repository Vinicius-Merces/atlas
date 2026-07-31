from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path, PurePosixPath

from release_utils import (
    canonical_release_bytes,
    is_release_path,
    sha256_bytes,
    source_payload,
    write_deterministic_zip,
    write_external_metadata,
)


ROOT = Path(__file__).resolve().parents[1]


def git_output(repository: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=repository,
        capture_output=True,
    )
    if result.returncode:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise SystemExit(message or f"git {' '.join(args)} failed")
    return result.stdout


def git_payload(repository: Path, reference: str) -> dict[str, bytes]:
    names = git_output(
        repository, "ls-tree", "-r", "--name-only", "-z", reference
    )
    payload: dict[str, bytes] = {}
    for raw in names.split(b"\0"):
        if not raw:
            continue
        relative = raw.decode("utf-8").replace("\\", "/")
        if not is_release_path(PurePosixPath(relative)):
            continue
        payload[relative] = canonical_release_bytes(
            git_output(repository, "show", f"{reference}:{relative}")
        )
    return payload


def base_state(
    source_root: Path, base: str
) -> tuple[str, dict[str, bytes]]:
    base_path = Path(base)
    if base_path.is_dir():
        resolved = base_path.resolve()
        version = (resolved / "VERSION").read_text(encoding="utf-8").strip()
        return version, source_payload(resolved)
    version = git_output(source_root, "show", f"{base}:VERSION").decode(
        "utf-8"
    ).strip()
    return version, git_payload(source_root, base)


def package_path(target_path: str) -> str:
    if target_path.startswith(".claude/"):
        return "CLAUDE-DIRECTORY/" + target_path.removeprefix(".claude/")
    return target_path


def markdown_list(
    title: str,
    paths: list[tuple[str, str | None]],
) -> bytes:
    lines = [f"# {title}", ""]
    if not paths:
        lines.append("_None._")
    else:
        for package, target in paths:
            if target is None or package == target:
                lines.append(f"- `{package}`")
            else:
                lines.append(f"- `{package}` → `{target}`")
    lines.append("")
    return "\n".join(lines).encode("utf-8")


def apply_instructions(from_version: str, to_version: str) -> bytes:
    return f"""# Apply ATLAS Incremental Patch

Base version: `{from_version}`

Target version: `{to_version}`

1. Confirm the installed `VERSION` exactly matches the base version.
2. Extract this archive without renaming its versioned root.
3. Copy files listed in `FILES-TO-ADD.md`.
4. Copy and overwrite files listed in `FILES-TO-REPLACE.md`.
5. Map every `CLAUDE-DIRECTORY/...` path to `.claude/...`.
6. Remove only target paths explicitly listed in `FILES-TO-DELETE.md`.
7. Confirm `VERSION` matches the target version.
8. Run the documented validators if desired.

No script is required to apply this patch. Absence from the archive never
authorizes deletion.
""".encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    parser.add_argument("--source-root", default=str(ROOT))
    parser.add_argument("--output-dir")
    args = parser.parse_args()

    source_root = Path(args.source_root).resolve()
    output_dir = (
        Path(args.output_dir).resolve()
        if args.output_dir
        else source_root / "dist"
    )
    to_version = (source_root / "VERSION").read_text(encoding="utf-8").strip()
    from_version, base_payload = base_state(source_root, args.base)
    current_payload = source_payload(source_root)
    if from_version == to_version:
        raise SystemExit("Incremental release requires distinct base and target versions")

    added = sorted(set(current_payload) - set(base_payload))
    deleted = sorted(set(base_payload) - set(current_payload))
    modified = sorted(
        path
        for path in set(current_payload) & set(base_payload)
        if current_payload[path] != base_payload[path]
    )

    operations = []
    package_payload: dict[str, bytes] = {}
    for operation, paths in [("add", added), ("replace", modified)]:
        for target in paths:
            packaged = package_path(target)
            content = current_payload[target]
            package_payload[packaged] = content
            operations.append(
                {
                    "path": target,
                    "target_path": target,
                    "package_path": packaged,
                    "operation": operation,
                    "sha256": sha256_bytes(content),
                }
            )
    for target in deleted:
        operations.append(
            {
                "path": target,
                "target_path": target,
                "package_path": "",
                "operation": "delete",
            }
        )
    operations.sort(key=lambda item: (item["target_path"], item["operation"]))

    patch_manifest = {
        "package_type": "incremental",
        "deployment_mode": "manual-copy-supported",
        "from_version": from_version,
        "to_version": to_version,
        "directory_mappings": {"CLAUDE-DIRECTORY": ".claude"},
        "added_count": len(added),
        "modified_count": len(modified),
        "deleted_count": len(deleted),
        "files": operations,
    }
    package_payload.update(
        {
            "APPLY-PATCH.md": apply_instructions(from_version, to_version),
            "PATCH-MANIFEST.json": (
                json.dumps(patch_manifest, indent=2) + "\n"
            ).encode("utf-8"),
            "FILES-TO-ADD.md": markdown_list(
                "Files to Add",
                [(package_path(path), path) for path in added],
            ),
            "FILES-TO-REPLACE.md": markdown_list(
                "Files to Replace",
                [(package_path(path), path) for path in modified],
            ),
            "FILES-TO-DELETE.md": markdown_list(
                "Files to Delete",
                [(path, None) for path in deleted],
            ),
        }
    )

    root_name = f"atlas-framework-{to_version}-incremental"
    archive_path = output_dir / f"{root_name}.zip"
    manifest_bytes = write_deterministic_zip(
        archive_path, root_name, package_payload
    )
    manifest_path, checksum_path = write_external_metadata(
        archive_path,
        "incremental",
        to_version,
        manifest_bytes,
        len(package_payload),
        from_version=from_version,
    )

    print(
        f"Created {archive_path}: "
        f"{len(added)} added, {len(modified)} modified, {len(deleted)} deleted"
    )
    print(f"Created {manifest_path}")
    print(f"Created {checksum_path}")


if __name__ == "__main__":
    main()
