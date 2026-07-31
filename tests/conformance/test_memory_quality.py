from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, f"scripts/{script}", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_canonical_memory_is_owned_sourced_and_fresh() -> None:
    result = run("validate_memory_freshness.py", "--strict")
    assert result.returncode == 0, result.stdout + result.stderr


def test_memory_and_obsidian_links_resolve() -> None:
    result = run("validate_knowledge_links.py")
    assert result.returncode == 0, result.stdout + result.stderr
