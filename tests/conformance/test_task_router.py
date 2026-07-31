from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def route(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/atlas_route.py", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_router_preserves_operational_context() -> None:
    result = route(
        "--task-type",
        "integration",
        "--summary",
        "Add a payment provider",
        "--risk",
        "high",
        "--runtime",
        "codex",
        "--path",
        "src/payments",
        "--acceptance",
        "Retries are idempotent",
        "--constraint",
        "No breaking API change",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    envelope = json.loads(result.stdout)
    assert envelope["route_source"] == "matched"
    assert envelope["primary_role"] == "integration-engineer"
    assert envelope["workflow"] == "integration-onboarding"
    assert envelope["risk"] == "high"
    assert envelope["runtime"] == "codex"
    assert envelope["affected_paths"] == ["src/payments"]
    assert envelope["acceptance_criteria"] == ["Retries are idempotent"]
    assert envelope["constraints"] == ["No breaking API change"]
    assert "governance-review" in envelope["reviews"]


def test_unknown_task_type_uses_explicit_fallback() -> None:
    result = route(
        "--task-type",
        "unclassified",
        "--summary",
        "Inspect an unusual request",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    envelope = json.loads(result.stdout)
    assert envelope["route_source"] == "fallback"
    assert envelope["primary_role"] == "orchestrator"
    assert envelope["workflow"] == "default"
