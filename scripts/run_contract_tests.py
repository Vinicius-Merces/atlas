from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    command = [sys.executable, "-m", "pytest", "tests/contract", "-q"]
    result = subprocess.run(command, cwd=ROOT)
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
