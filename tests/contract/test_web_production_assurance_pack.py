from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_web_production_assurance_pack_contract() -> None:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_web_production_assurance_pack.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
