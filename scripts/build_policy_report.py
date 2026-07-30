from __future__ import annotations
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/evaluate_policies.py")],
        cwd=ROOT,
    )
    raise SystemExit(result.returncode)

if __name__ == "__main__":
    main()
