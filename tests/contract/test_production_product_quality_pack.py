from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_production_product_quality_pack_validator() -> None:
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_production_product_quality_pack.py")], cwd=ROOT, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "7 skills" in result.stdout


def test_p1_is_skill_expansion_not_agent_inflation() -> None:
    registry = json.loads((ROOT / ".claude" / "registry.json").read_text(encoding="utf-8"))
    assert len(registry["agents"]) + 1 == 87
