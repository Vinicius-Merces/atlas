from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", required=True)
    parser.add_argument("--output-root", required=True)
    args = parser.parse_args()

    archive = Path(args.archive).resolve()
    output = Path(args.output_root).resolve()
    if output.exists():
        raise SystemExit("Simulation output root must not already exist")

    validation = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_release_artifacts.py"),
            "--archive",
            str(archive),
        ],
        cwd=ROOT,
    )
    if validation.returncode:
        raise SystemExit(validation.returncode)

    with tempfile.TemporaryDirectory() as temporary:
        extraction = Path(temporary)
        with ZipFile(archive) as package:
            package.extractall(extraction)
        roots = list(extraction.iterdir())
        if len(roots) != 1 or not roots[0].is_dir():
            raise SystemExit("Cumulative package has an invalid versioned root")
        shutil.copytree(roots[0], output)

    if not (output / ".claude" / "registry.json").is_file():
        raise SystemExit("Clean install is missing .claude/registry.json")
    if not (output / "VERSION").is_file():
        raise SystemExit("Clean install is missing VERSION")
    print(f"Cumulative install simulation passed: {output}")


if __name__ == "__main__":
    main()
