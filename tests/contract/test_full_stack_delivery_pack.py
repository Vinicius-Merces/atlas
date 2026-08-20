from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
P2_AGENT_SURFACE_BASELINE = 87


def test_full_stack_delivery_pack_validator() -> None:
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_full_stack_delivery_pack.py")], cwd=ROOT, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "11 skills" in result.stdout
    assert "6 blueprints" in result.stdout


def test_p2_preserves_agent_surface() -> None:
    registry = json.loads((ROOT / ".claude" / "registry.json").read_text(encoding="utf-8"))
    current_surface = len(registry["agents"]) + 1
    assert current_surface >= P2_AGENT_SURFACE_BASELINE


def test_p2_requires_premium_frontend_inheritance() -> None:
    model = (ROOT / "framework" / "full-stack-delivery-model.md").read_text(encoding="utf-8")
    assert "Every user-facing blueprint inherits Frontend Craft" in model
