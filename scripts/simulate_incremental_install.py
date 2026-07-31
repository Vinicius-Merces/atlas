from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import re
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]


def safe_target(root: Path, relative: str) -> Path:
    pure = PurePosixPath(relative.replace("\\", "/"))
    if (
        pure.is_absolute()
        or ".." in pure.parts
        or not relative
        or "\\" in relative
        or re.match(r"^[A-Za-z]:", relative)
    ):
        raise SystemExit(f"Unsafe target path: {relative}")
    target = (root / Path(*pure.parts)).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        raise SystemExit(f"Target escapes installation root: {relative}") from None
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--installed-root", required=True)
    parser.add_argument("--patch-root", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()

    installed = Path(args.installed_root).resolve()
    patch = Path(args.patch_root).resolve()
    output = Path(args.output_root).resolve()
    if output.exists():
        raise SystemExit("Simulation output root must not already exist")

    preflight = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "manual_deploy_preflight.py"),
            "--installed-root",
            str(installed),
            "--patch-root",
            str(patch),
        ],
        cwd=ROOT,
    )
    if preflight.returncode:
        raise SystemExit(preflight.returncode)

    shutil.copytree(installed, output)
    manifest = json.loads(
        (patch / "PATCH-MANIFEST.json").read_text(encoding="utf-8")
    )
    deleted_parents: set[Path] = set()
    for item in manifest["files"]:
        operation = item["operation"]
        target = safe_target(output, item["target_path"])
        if operation in {"add", "replace"}:
            source = patch / item["package_path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        elif operation == "delete":
            if target.is_dir():
                raise SystemExit(
                    f"Recursive directory deletion is not supported: {item['target_path']}"
                )
            if target.exists():
                target.unlink()
            deleted_parents.add(target.parent)
        else:
            raise SystemExit(f"Unsupported operation: {operation}")

    for directory in sorted(
        deleted_parents,
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        current = directory
        while current != output and current.is_relative_to(output):
            try:
                current.rmdir()
            except OSError:
                break
            current = current.parent

    actual = (output / "VERSION").read_text(encoding="utf-8").strip()
    if actual != manifest["to_version"]:
        raise SystemExit(
            f"Simulation produced VERSION {actual}, expected {manifest['to_version']}"
        )
    print(f"Incremental install simulation passed: {output}")


if __name__ == "__main__":
    main()
