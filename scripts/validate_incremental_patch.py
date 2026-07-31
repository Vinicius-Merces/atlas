from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: validate_incremental_patch.py <installed-root> <patch-root>"
        )
    installed = Path(sys.argv[1]).resolve()
    patch = Path(sys.argv[2]).resolve()
    result = subprocess.run(
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
    if result.returncode:
        raise SystemExit(result.returncode)

    manifest = json.loads(
        (patch / "PATCH-MANIFEST.json").read_text(encoding="utf-8")
    )
    print(
        f"Patch valid: {manifest['from_version']} -> {manifest['to_version']} "
        f"({len(manifest['files'])} operations)"
    )


if __name__ == "__main__":
    main()
