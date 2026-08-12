from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate_capability_taxonomy.py"


def test_capability_taxonomy_contract() -> None:
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    output = "\n".join(
        part.strip() for part in (completed.stdout, completed.stderr) if part.strip()
    )
    assert completed.returncode == 0, output
    assert "87 agents" in completed.stdout
    assert "13 domains" in completed.stdout
    assert "88 registered skills" in completed.stdout
