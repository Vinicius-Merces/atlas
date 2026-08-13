from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_agent_and_skill_discovery_metadata() -> None:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_discovery_metadata.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "Discovery metadata valid:" in completed.stdout
