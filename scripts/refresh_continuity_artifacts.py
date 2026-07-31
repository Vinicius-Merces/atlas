from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str, *args: str) -> None:
    command = [sys.executable, str(ROOT / "scripts" / script), *args]
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode:
        raise SystemExit(result.returncode)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Refresh ATLAS continuity artifacts in dependency order."
    )
    parser.parse_args(argv)

    run("build_project_brief.py")
    run("build_resume_packet.py")
    run("audit_memory_drift.py")
    print("Continuity artifacts refreshed.")


if __name__ == "__main__":
    main()
