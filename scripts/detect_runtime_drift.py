from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    errors: list[str] = []

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    codex_manifest = json.loads(
        (ROOT / "adapters/codex/runtime-manifest.json").read_text(encoding="utf-8")
    )
    if codex_manifest.get("version") != version:
        errors.append("Codex runtime version differs from framework version")

    result = subprocess.run(
        [sys.executable, "scripts/sync_codex_adapter.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        errors.append(result.stdout.strip() or result.stderr.strip())

    if errors:
        print("Runtime drift detected:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("No blocking runtime drift detected.")


if __name__ == "__main__":
    main()
