from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_saas_production_trust_pack_contract() -> None:
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_saas_production_trust_pack.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "SaaS production trust pack valid:" in completed.stdout
