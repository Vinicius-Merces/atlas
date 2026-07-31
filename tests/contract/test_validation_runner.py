from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import validate_all


ROOT = Path(__file__).resolve().parents[2]


def test_help_exposes_portable_profiles() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_all.py", "--help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "--profile {quick,full,release}" in result.stdout
    assert "--incremental-base" in result.stdout
    assert "--list" in result.stdout


def test_profiles_are_layered_and_release_keeps_every_full_gate() -> None:
    quick = validate_all.build_profile("quick", ROOT)
    full = validate_all.build_profile("full", ROOT)
    release = validate_all.build_profile(
        "release",
        ROOT,
        skip_incremental=True,
    )

    quick_keys = [step.key for step in quick]
    full_keys = [step.key for step in full]
    release_keys = [step.key for step in release]

    assert full_keys[: len(quick_keys)] == quick_keys
    assert release_keys[: len(full_keys)] == full_keys
    assert {
        "compile-scripts",
        "validate-json",
        "validate-yaml",
        "registry",
        "contracts",
        "native-skills-sync",
        "policies",
        "smoke-tests",
        "contract-tests",
        "codex-tests",
        "conformance-tests",
        "full-tests",
    } <= set(full_keys)
    assert release_keys[-4:] == [
        "build-cumulative",
        "validate-cumulative",
        "build-recovery",
        "validate-recovery",
    ]


def test_release_profile_resolves_declared_incremental_base() -> None:
    release = validate_all.build_profile("release", ROOT)
    keys = [step.key for step in release]
    incremental = next(step for step in release if step.key == "build-incremental")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    manifest = json.loads(
        (ROOT / "release" / f"{version}.manifest.json").read_text(
            encoding="utf-8"
        )
    )
    declared_base = (
        manifest.get("incremental_base_commit")
        or manifest["incremental_base"]
    )

    assert keys[-2:] == ["build-incremental", "validate-incremental"]
    assert incremental.command is not None
    assert declared_base in incremental.command


def test_runner_is_fail_fast_by_default() -> None:
    steps = [
        validate_all.ValidationStep("first", "First", command=("first",)),
        validate_all.ValidationStep("second", "Second", command=("second",)),
        validate_all.ValidationStep("third", "Third", command=("third",)),
    ]
    seen: list[str] = []

    def executor(command: list[str], *, cwd: Path) -> SimpleNamespace:
        assert cwd == ROOT
        seen.append(command[0])
        return SimpleNamespace(returncode=1 if command[0] == "second" else 0)

    results = validate_all.run_steps(steps, ROOT, executor=executor)

    assert seen == ["first", "second"]
    assert [result.returncode for result in results] == [0, 1]


def test_in_process_data_validation_rejects_invalid_files(tmp_path: Path) -> None:
    (tmp_path / "valid.json").write_text('{"ok": true}\n', encoding="utf-8")
    (tmp_path / "broken.json").write_text("{", encoding="utf-8")

    with pytest.raises(validate_all.ValidationFailure, match="broken.json"):
        validate_all.validate_json_files(tmp_path)


def test_data_validation_ignores_generated_distribution_trees(
    tmp_path: Path,
) -> None:
    (tmp_path / "valid.json").write_text('{"ok": true}\n', encoding="utf-8")
    generated = tmp_path / "dist" / "installed"
    generated.mkdir(parents=True)
    (generated / "stale.json").write_text("{", encoding="utf-8")

    result = validate_all.validate_json_files(tmp_path)

    assert result == "JSON validation passed: 1 file"
