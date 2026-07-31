from __future__ import annotations

import argparse
import compileall
import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ("quick", "full", "release")
EXCLUDED_SCAN_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "dist",
    "venv",
}


class ValidationFailure(RuntimeError):
    """Raised when an in-process validation step fails."""


@dataclass(frozen=True)
class ValidationStep:
    key: str
    description: str
    command: tuple[str, ...] | None = None
    action: Callable[[Path], str] | None = None

    def __post_init__(self) -> None:
        if (self.command is None) == (self.action is None):
            raise ValueError("A validation step must define exactly one execution mode")


@dataclass(frozen=True)
class StepResult:
    key: str
    returncode: int
    duration_seconds: float


def _repository_files(root: Path, suffixes: set[str]) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix.lower() in suffixes
        and not (
            set(path.relative_to(root).parts)
            & EXCLUDED_SCAN_PARTS
        )
    )


def compile_scripts(root: Path) -> str:
    if not compileall.compile_dir(str(root / "scripts"), quiet=1):
        raise ValidationFailure("Python script compilation failed")
    return "Python script compilation passed"


def validate_json_files(root: Path) -> str:
    paths = _repository_files(root, {".json"})
    failures: list[str] = []
    for path in paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"{path.relative_to(root).as_posix()}: {exc}")
    if failures:
        raise ValidationFailure(
            "JSON validation failed:\n" + "\n".join(f"- {item}" for item in failures)
        )
    noun = "file" if len(paths) == 1 else "files"
    return f"JSON validation passed: {len(paths)} {noun}"


def validate_yaml_files(root: Path) -> str:
    try:
        import yaml
    except ImportError as exc:
        raise ValidationFailure(
            "PyYAML is required; install requirements-test.txt"
        ) from exc

    paths = _repository_files(root, {".yml", ".yaml"})
    failures: list[str] = []
    for path in paths:
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"{path.relative_to(root).as_posix()}: {exc}")
    if failures:
        raise ValidationFailure(
            "YAML validation failed:\n" + "\n".join(f"- {item}" for item in failures)
        )
    noun = "file" if len(paths) == 1 else "files"
    return f"YAML validation passed: {len(paths)} {noun}"


def _python_step(
    root: Path,
    key: str,
    description: str,
    script: str,
    *arguments: str,
) -> ValidationStep:
    return ValidationStep(
        key=key,
        description=description,
        command=(
            sys.executable,
            str(root / "scripts" / script),
            *arguments,
        ),
    )


def quick_steps(root: Path) -> list[ValidationStep]:
    return [
        ValidationStep(
            "compile-scripts",
            "Compile Python scripts",
            action=compile_scripts,
        ),
        ValidationStep(
            "validate-json",
            "Parse repository JSON",
            action=validate_json_files,
        ),
        ValidationStep(
            "validate-yaml",
            "Parse repository YAML",
            action=validate_yaml_files,
        ),
        _python_step(
            root,
            "version",
            "Validate version consistency",
            "manage_version.py",
        ),
        _python_step(
            root,
            "schemas",
            "Validate schemas and fixtures",
            "validate_schemas.py",
        ),
        _python_step(
            root,
            "registry",
            "Validate registry",
            "validate_registry.py",
        ),
        _python_step(
            root,
            "package",
            "Validate package source",
            "validate_package.py",
        ),
        _python_step(
            root,
            "contracts",
            "Validate canonical contracts",
            "validate_contracts.py",
        ),
    ]


def full_steps(
    root: Path,
    *,
    policy_output: str = "-",
) -> list[ValidationStep]:
    return [
        *quick_steps(root),
        _python_step(
            root,
            "codex-adapter",
            "Validate Codex adapter",
            "validate_codex_adapter.py",
        ),
        _python_step(
            root,
            "codex-sync",
            "Check Codex synchronization",
            "sync_codex_adapter.py",
            "--check",
        ),
        _python_step(
            root,
            "native-skills-sync",
            "Check native skill synchronization",
            "sync_native_skills.py",
            "--check",
        ),
        _python_step(
            root,
            "runtime-drift",
            "Detect runtime drift",
            "detect_runtime_drift.py",
        ),
        _python_step(
            root,
            "runtime-contract",
            "Validate universal runtime contract",
            "validate_runtime_contract.py",
        ),
        _python_step(
            root,
            "runtime-conformance",
            "Validate runtime conformance",
            "validate_conformance.py",
        ),
        _python_step(
            root,
            "source-of-truth",
            "Validate canonical sources of truth",
            "validate_source_of_truth.py",
        ),
        _python_step(
            root,
            "memory-freshness",
            "Validate memory freshness",
            "validate_memory_freshness.py",
            "--strict",
        ),
        _python_step(
            root,
            "knowledge-links",
            "Validate memory and Obsidian links",
            "validate_knowledge_links.py",
        ),
        _python_step(
            root,
            "documentation",
            "Validate documentation",
            "validate_documentation.py",
        ),
        _python_step(
            root,
            "policy-exceptions",
            "Validate policy exceptions",
            "validate_policy_exceptions.py",
        ),
        _python_step(
            root,
            "policies",
            "Evaluate policy rules",
            "evaluate_policies.py",
            "--output",
            policy_output,
        ),
        _python_step(
            root,
            "smoke-tests",
            "Run smoke tests",
            "run_smoke_tests.py",
        ),
        _python_step(
            root,
            "contract-tests",
            "Run contract tests",
            "run_contract_tests.py",
        ),
        _python_step(
            root,
            "codex-tests",
            "Run Codex tests",
            "run_codex_tests.py",
        ),
        _python_step(
            root,
            "conformance-tests",
            "Run conformance tests",
            "run_conformance_tests.py",
        ),
        ValidationStep(
            "full-tests",
            "Run the full automated test suite",
            command=(
                sys.executable,
                "-m",
                "pytest",
                "tests",
                "-q",
            ),
        ),
    ]


def resolve_incremental_base(root: Path, explicit: str | None) -> str | None:
    if explicit:
        return explicit
    version_path = root / "VERSION"
    if not version_path.is_file():
        return None
    version = version_path.read_text(encoding="utf-8").strip()
    release_manifest = root / "release" / f"{version}.manifest.json"
    if not release_manifest.is_file():
        return None
    data = json.loads(release_manifest.read_text(encoding="utf-8"))
    return data.get("incremental_base_commit") or data.get("incremental_base")


def release_steps(
    root: Path,
    *,
    output_dir: Path,
    incremental_base: str | None,
    skip_incremental: bool,
) -> list[ValidationStep]:
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    output_dir = output_dir.resolve()
    cumulative = output_dir / f"atlas-framework-{version}-cumulative.zip"
    recovery = output_dir / f"atlas-framework-{version}-recovery.zip"
    steps = [
        _python_step(
            root,
            "build-cumulative",
            "Build cumulative release dry-run",
            "build_release.py",
            "--kind",
            "cumulative",
            "--output-dir",
            str(output_dir),
        ),
        _python_step(
            root,
            "validate-cumulative",
            "Validate cumulative release dry-run",
            "validate_release_artifacts.py",
            "--archive",
            str(cumulative),
        ),
        _python_step(
            root,
            "build-recovery",
            "Build recovery release dry-run",
            "build_release.py",
            "--kind",
            "recovery",
            "--output-dir",
            str(output_dir),
        ),
        _python_step(
            root,
            "validate-recovery",
            "Validate recovery release dry-run",
            "validate_release_artifacts.py",
            "--archive",
            str(recovery),
        ),
    ]
    if skip_incremental:
        return steps
    if not incremental_base:
        raise ValidationFailure(
            "The release profile requires an incremental base. Pass "
            "--incremental-base, add incremental_base_commit to the "
            "version-specific release manifest, or explicitly use "
            "--skip-incremental."
        )
    incremental = output_dir / f"atlas-framework-{version}-incremental.zip"
    steps.extend(
        [
            _python_step(
                root,
                "build-incremental",
                "Build incremental release dry-run",
                "build_incremental_release.py",
                "--base",
                incremental_base,
                "--output-dir",
                str(output_dir),
            ),
            _python_step(
                root,
                "validate-incremental",
                "Validate incremental release dry-run",
                "validate_release_artifacts.py",
                "--archive",
                str(incremental),
            ),
        ]
    )
    return steps


def build_profile(
    profile: str,
    root: Path,
    *,
    output_dir: Path | None = None,
    incremental_base: str | None = None,
    skip_incremental: bool = False,
    policy_output: str = "-",
) -> list[ValidationStep]:
    if profile not in PROFILES:
        raise ValueError(f"Unknown profile: {profile}")
    if profile == "quick":
        return quick_steps(root)
    steps = full_steps(root, policy_output=policy_output)
    if profile == "full":
        return steps
    resolved_base = resolve_incremental_base(root, incremental_base)
    return [
        *steps,
        *release_steps(
            root,
            output_dir=output_dir or root / "dist",
            incremental_base=resolved_base,
            skip_incremental=skip_incremental,
        ),
    ]


def run_steps(
    steps: Sequence[ValidationStep],
    root: Path,
    *,
    keep_going: bool = False,
    executor: Callable[..., subprocess.CompletedProcess[object]] = subprocess.run,
) -> list[StepResult]:
    results: list[StepResult] = []
    for index, step in enumerate(steps, start=1):
        print(f"[{index}/{len(steps)}] {step.description}", flush=True)
        started = time.monotonic()
        returncode = 0
        try:
            if step.action is not None:
                message = step.action(root)
                if message:
                    print(message, flush=True)
            else:
                if step.command is None:
                    raise ValidationFailure(
                        f"Step {step.key} has no command or action"
                    )
                completed = executor(list(step.command), cwd=root)
                returncode = completed.returncode
        except (OSError, ValidationFailure) as exc:
            print(f"ERROR: {exc}", flush=True)
            returncode = 1
        duration = time.monotonic() - started
        results.append(
            StepResult(
                key=step.key,
                returncode=returncode,
                duration_seconds=duration,
            )
        )
        outcome = "passed" if returncode == 0 else "failed"
        print(f"{step.key}: {outcome} ({duration:.2f}s)", flush=True)
        if returncode and not keep_going:
            break
    return results


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description=(
            "Run ATLAS validation through portable quick, full, or release "
            "profiles without shell-specific orchestration."
        )
    )
    result.add_argument(
        "--profile",
        choices=PROFILES,
        default="quick",
        help=(
            "quick runs foundational gates; full adds runtime, policy, and "
            "test gates; release adds cumulative, recovery, and incremental "
            "artifact dry-runs"
        ),
    )
    result.add_argument(
        "--root",
        default=str(ROOT),
        help="Repository root to validate (default: the repository containing this script)",
    )
    result.add_argument(
        "--output-dir",
        help="Release artifact output directory (release profile only)",
    )
    result.add_argument(
        "--incremental-base",
        help=(
            "Directory or Git ref for the incremental release base. When "
            "omitted, the version-specific release manifest is consulted."
        ),
    )
    result.add_argument(
        "--skip-incremental",
        action="store_true",
        help="Explicitly omit incremental packaging from the release profile",
    )
    result.add_argument(
        "--keep-going",
        action="store_true",
        help="Run remaining steps after a failure and report all failures",
    )
    result.add_argument(
        "--policy-output",
        default="-",
        help=(
            "Policy report path for full/release profiles. The default '-' "
            "prints the report without modifying the repository."
        ),
    )
    result.add_argument(
        "--list",
        action="store_true",
        help="List the selected profile steps without executing them",
    )
    return result


def main() -> None:
    args = parser().parse_args()
    root = Path(args.root).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else None
    try:
        steps = build_profile(
            args.profile,
            root,
            output_dir=output_dir,
            incremental_base=args.incremental_base,
            skip_incremental=args.skip_incremental,
            policy_output=args.policy_output,
        )
    except (OSError, ValueError, json.JSONDecodeError, ValidationFailure) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

    if args.list:
        for step in steps:
            print(f"{step.key}: {step.description}")
        return

    print(
        f"ATLAS validation profile: {args.profile} ({len(steps)} steps)",
        flush=True,
    )
    results = run_steps(steps, root, keep_going=args.keep_going)
    failures = [result for result in results if result.returncode]
    completed = len(results)
    print(
        "Validation summary: "
        f"completed={completed}, passed={completed - len(failures)}, "
        f"failed={len(failures)}"
    )
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
