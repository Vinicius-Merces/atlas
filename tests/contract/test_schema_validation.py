from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_every_schema_has_a_valid_fixture() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_schemas.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
