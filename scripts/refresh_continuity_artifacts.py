from __future__ import annotations
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(script: str, *args: str) -> None:
    command = [sys.executable, str(ROOT / "scripts" / script), *args]
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode:
        raise SystemExit(result.returncode)

def main() -> None:
    run("build_project_brief.py")
    run("build_resume_packet.py")
    run("audit_memory_drift.py")
    print("Continuity artifacts refreshed.")

if __name__ == "__main__":
    main()
