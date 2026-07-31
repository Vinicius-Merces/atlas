from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def prepare(tmp_path: Path, *, omit_codex_capability: bool) -> Path:
    root = tmp_path / "runtime"
    (root / "adapters" / "shared").mkdir(parents=True)
    (root / "adapters" / "claude").mkdir()
    (root / "adapters" / "codex").mkdir()
    (root / ".claude").mkdir()
    (root / "framework").mkdir()
    (root / "VERSION").write_text("1.0.0\n", encoding="utf-8")
    contract = {
        "version": "1.0.0",
        "required_capabilities": ["read-files", "validate"],
        "shared_sources": {
            "framework": "framework",
        },
    }
    (root / "adapters/shared/runtime-contract.json").write_text(
        json.dumps(contract),
        encoding="utf-8",
    )
    for runtime, implementation in (
        ("claude", ".claude"),
        ("codex", "adapters/codex"),
    ):
        capabilities = ["read-files", "validate"]
        if runtime == "codex" and omit_codex_capability:
            capabilities.remove("validate")
        declaration = {
            "version": "1.0.0",
            "capabilities": capabilities,
            "implementation": implementation,
        }
        (root / f"adapters/{runtime}/runtime-declaration.json").write_text(
            json.dumps(declaration),
            encoding="utf-8",
        )
    return root


def run_optimized(script: str, root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-O",
            str(ROOT / "scripts" / script),
            "--root",
            str(root),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_runtime_validators_pass_under_optimized_python(tmp_path: Path) -> None:
    root = prepare(tmp_path, omit_codex_capability=False)
    for script in ("validate_runtime_contract.py", "validate_conformance.py"):
        result = run_optimized(script, root)
        assert result.returncode == 0, result.stdout + result.stderr


def test_runtime_validators_still_block_under_optimized_python(
    tmp_path: Path,
) -> None:
    root = prepare(tmp_path, omit_codex_capability=True)
    for script in ("validate_runtime_contract.py", "validate_conformance.py"):
        result = run_optimized(script, root)
        assert result.returncode == 1
        assert "missing capabilities: validate" in result.stdout
