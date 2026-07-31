from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_release_artifacts import safe_path


def run(script: str, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == expected, result.stdout + result.stderr
    return result


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_cumulative_and_recovery_packages_are_reproducible(
    tmp_path: Path,
) -> None:
    output = tmp_path / "dist"
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    cumulative = output / f"atlas-framework-{version}-cumulative.zip"
    recovery = output / f"atlas-framework-{version}-recovery.zip"

    run("build_release.py", "--output-dir", str(output), "--kind", "cumulative")
    first_hash = digest(cumulative)
    run("validate_release_artifacts.py", "--archive", str(cumulative))
    run("build_release.py", "--output-dir", str(output), "--kind", "cumulative")
    assert digest(cumulative) == first_hash

    installed = tmp_path / "installed"
    run(
        "simulate_cumulative_install.py",
        "--archive",
        str(cumulative),
        "--output-root",
        str(installed),
    )
    assert (installed / ".claude" / "registry.json").is_file()
    assert not (installed / ".vscode").exists()
    assert not (installed / ".atlas").exists()
    assert not (installed / "reports").exists()

    run("build_release.py", "--output-dir", str(output), "--kind", "recovery")
    run("validate_release_artifacts.py", "--archive", str(recovery))
    recovered = tmp_path / "recovered"
    run(
        "simulate_cumulative_install.py",
        "--archive",
        str(recovery),
        "--output-root",
        str(recovered),
    )
    assert (recovered / "RECOVERY-INSTRUCTIONS.md").is_file()


def prepare_incremental_roots(tmp_path: Path) -> tuple[Path, Path]:
    base = tmp_path / "base"
    current = tmp_path / "current"
    (base / ".claude" / "agents").mkdir(parents=True)
    (current / ".claude" / "agents").mkdir(parents=True)
    (base / "VERSION").write_text("0.1.0-beta.11\n", encoding="utf-8")
    (current / "VERSION").write_text("0.1.0-rc.1\n", encoding="utf-8")
    (base / ".claude" / "agents" / "old.md").write_text(
        "old\n", encoding="utf-8"
    )
    (current / ".claude" / "agents" / "old.md").write_text(
        "updated\n", encoding="utf-8"
    )
    (current / ".claude" / "agents" / "new.md").write_text(
        "new\n", encoding="utf-8"
    )
    for root in [base, current]:
        (root / "keep.txt").write_text("keep\n", encoding="utf-8")
        (root / "unrelated.txt").write_text("preserve\n", encoding="utf-8")
    (base / "line-endings.txt").write_bytes(b"same\r\n")
    (current / "line-endings.txt").write_bytes(b"same\n")
    (base / "delete.txt").write_text("delete\n", encoding="utf-8")
    (base / "obsolete" / "nested").mkdir(parents=True)
    (base / "obsolete" / "nested" / "only.txt").write_text(
        "delete\n", encoding="utf-8"
    )
    return base, current


def test_incremental_upgrade_maps_hidden_directory_and_deletes_explicitly(
    tmp_path: Path,
) -> None:
    base, current = prepare_incremental_roots(tmp_path)
    output = tmp_path / "dist"
    archive = output / "atlas-framework-0.1.0-rc.1-incremental.zip"
    run(
        "build_incremental_release.py",
        "--base",
        str(base),
        "--source-root",
        str(current),
        "--output-dir",
        str(output),
    )
    first_hash = digest(archive)
    run("validate_release_artifacts.py", "--archive", str(archive))
    run(
        "build_incremental_release.py",
        "--base",
        str(base),
        "--source-root",
        str(current),
        "--output-dir",
        str(output),
    )
    assert digest(archive) == first_hash

    extraction = tmp_path / "extracted"
    with ZipFile(archive) as package:
        package.extractall(extraction)
    roots = list(extraction.iterdir())
    assert len(roots) == 1
    patch = roots[0]
    assert (patch / "CLAUDE-DIRECTORY" / "agents" / "new.md").is_file()
    assert not (patch / ".claude").exists()
    manifest = json.loads(
        (patch / "PATCH-MANIFEST.json").read_text(encoding="utf-8")
    )
    assert "line-endings.txt" not in {
        item["target_path"] for item in manifest["files"]
    }

    upgraded = tmp_path / "upgraded"
    run(
        "simulate_incremental_install.py",
        "--installed-root",
        str(base),
        "--patch-root",
        str(patch),
        "--output-root",
        str(upgraded),
    )
    assert (upgraded / "VERSION").read_text(encoding="utf-8").strip() == "0.1.0-rc.1"
    assert (upgraded / ".claude" / "agents" / "new.md").is_file()
    assert (
        upgraded / ".claude" / "agents" / "old.md"
    ).read_text(encoding="utf-8") == "updated\n"
    assert not (upgraded / "delete.txt").exists()
    assert not (upgraded / "obsolete").exists()
    assert (upgraded / "unrelated.txt").read_text(encoding="utf-8") == "preserve\n"


def test_external_checksum_tampering_is_detected(tmp_path: Path) -> None:
    output = tmp_path / "dist"
    run("build_release.py", "--output-dir", str(output), "--kind", "cumulative")
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    archive = output / f"atlas-framework-{version}-cumulative.zip"
    checksum = archive.with_suffix(".sha256")
    checksum.write_text("0" * 64 + f"  {archive.name}\n", encoding="utf-8")
    run(
        "validate_release_artifacts.py",
        "--archive",
        str(archive),
        expected=1,
    )


def test_incremental_manifest_protects_replace_and_delete_bases(
    tmp_path: Path,
) -> None:
    base, current = prepare_incremental_roots(tmp_path)
    output = tmp_path / "dist"
    archive = output / "atlas-framework-0.1.0-rc.1-incremental.zip"
    run(
        "build_incremental_release.py",
        "--base",
        str(base),
        "--source-root",
        str(current),
        "--output-dir",
        str(output),
    )
    with ZipFile(archive) as package:
        root = package.namelist()[0].split("/", 1)[0]
        manifest = json.loads(
            package.read(f"{root}/PATCH-MANIFEST.json").decode("utf-8")
        )

    protected = [
        item
        for item in manifest["files"]
        if item["operation"] in {"replace", "delete"}
    ]
    assert protected
    assert all(len(item["base_sha256"]) == 64 for item in protected)
    assert len(manifest["base_content_manifest_sha256"]) == 64


def test_git_ignored_files_are_excluded_from_release_source(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=source, check=True)
    (source / "VERSION").write_text("1.0.0\n", encoding="utf-8")
    (source / "README.md").write_text("# Example\n", encoding="utf-8")
    (source / ".gitignore").write_text("local-only.txt\n", encoding="utf-8")
    (source / "local-only.txt").write_text("secret local state\n", encoding="utf-8")
    output = tmp_path / "dist"

    run(
        "build_release.py",
        "--source-root",
        str(source),
        "--output-dir",
        str(output),
    )

    archive = output / "atlas-framework-1.0.0-cumulative.zip"
    with ZipFile(archive) as package:
        assert not any(
            name.endswith("/local-only.txt") for name in package.namelist()
        )


def test_release_source_rejects_symlinks(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=source, check=True)
    (source / "VERSION").write_text("1.0.0\n", encoding="utf-8")
    target = source / "target.txt"
    target.write_text("target\n", encoding="utf-8")
    link = source / "link.txt"
    try:
        os.symlink(target, link)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks are unavailable in this environment")

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_release.py"),
            "--source-root",
            str(source),
            "--output-dir",
            str(tmp_path / "dist"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "cannot contain symlink" in result.stdout + result.stderr


@pytest.mark.parametrize(
    "value",
    [
        "../escape",
        "..\\escape",
        "/absolute",
        "\\\\server\\share",
        "C:\\absolute",
        "directory\\file.txt",
    ],
)
def test_release_validator_rejects_cross_platform_unsafe_paths(
    value: str,
) -> None:
    assert safe_path(value) is False
