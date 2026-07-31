from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def digest(path: Path) -> str:
    content = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(content).hexdigest()


def prepare(tmp_path: Path) -> tuple[Path, Path]:
    patch = tmp_path / "patch"
    installed = tmp_path / "installed"
    payload = patch / "CLAUDE-DIRECTORY" / "agents" / "example.md"
    payload.parent.mkdir(parents=True)
    payload.write_text("# Example\n", encoding="utf-8")
    installed.mkdir()
    (installed / "VERSION").write_text("0.1.0-beta.11\n", encoding="utf-8")
    manifest = {
        "from_version": "0.1.0-beta.11",
        "to_version": "0.1.0-rc.1",
        "directory_mappings": {"CLAUDE-DIRECTORY": ".claude"},
        "files": [
            {
                "path": ".claude/agents/example.md",
                "target_path": ".claude/agents/example.md",
                "package_path": "CLAUDE-DIRECTORY/agents/example.md",
                "operation": "add",
                "sha256": digest(payload),
            }
        ],
    }
    (patch / "PATCH-MANIFEST.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    (patch / "FILES-TO-ADD.md").write_text(
        "# Files to add\n\n- `CLAUDE-DIRECTORY/agents/example.md`\n",
        encoding="utf-8",
    )
    (patch / "FILES-TO-REPLACE.md").write_text(
        "# Files to replace\n\n", encoding="utf-8"
    )
    (patch / "FILES-TO-DELETE.md").write_text(
        "# Files to delete\n\n", encoding="utf-8"
    )
    return patch, installed


def run(patch: Path, installed: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "manual_deploy_preflight.py"),
            "--patch-root",
            str(patch),
            "--installed-root",
            str(installed),
        ],
        capture_output=True,
        text=True,
    )


def test_valid_manual_patch_passes_preflight(tmp_path: Path) -> None:
    patch, installed = prepare(tmp_path)
    result = run(patch, installed)
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(
        (patch / "DEPLOY-PREFLIGHT-REPORT.json").read_text(encoding="utf-8")
    )
    assert report["outcome"] == "passed"


def test_package_only_file_inside_visible_claude_directory_blocks(
    tmp_path: Path,
) -> None:
    patch, installed = prepare(tmp_path)
    (patch / "CLAUDE-DIRECTORY" / "PACKAGE-README.md").write_text(
        "Do not copy\n", encoding="utf-8"
    )
    result = run(patch, installed)
    assert result.returncode == 1
    report = json.loads(
        (patch / "DEPLOY-PREFLIGHT-REPORT.json").read_text(encoding="utf-8")
    )
    check = next(
        item for item in report["checks"] if item["check"] == "visible-payload-only"
    )
    assert check["passed"] is False


def test_wrong_installed_base_blocks_preflight(tmp_path: Path) -> None:
    patch, installed = prepare(tmp_path)
    (installed / "VERSION").write_text("0.1.0-beta.10\n", encoding="utf-8")
    result = run(patch, installed)
    assert result.returncode == 1


def test_existing_add_target_blocks_preflight(tmp_path: Path) -> None:
    patch, installed = prepare(tmp_path)
    target = installed / ".claude" / "agents" / "example.md"
    target.parent.mkdir(parents=True)
    target.write_text("project-owned customization\n", encoding="utf-8")

    result = run(patch, installed)

    assert result.returncode == 1
    report = json.loads(
        (patch / "DEPLOY-PREFLIGHT-REPORT.json").read_text(encoding="utf-8")
    )
    check = next(
        item for item in report["checks"] if item["check"] == "installed-state"
    )
    assert check["passed"] is False
    assert "add target already exists" in check["findings"][0]


def test_changed_replace_target_blocks_preflight(tmp_path: Path) -> None:
    patch, installed = prepare(tmp_path)
    source = installed / ".claude" / "agents" / "existing.md"
    source.parent.mkdir(parents=True)
    source.write_text("base\n", encoding="utf-8")
    payload = patch / "CLAUDE-DIRECTORY" / "agents" / "existing.md"
    payload.write_text("updated\n", encoding="utf-8")
    manifest_path = patch / "PATCH-MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"] = [
        {
            "path": ".claude/agents/existing.md",
            "target_path": ".claude/agents/existing.md",
            "package_path": "CLAUDE-DIRECTORY/agents/existing.md",
            "operation": "replace",
            "base_sha256": digest(source),
            "sha256": digest(payload),
        }
    ]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    (patch / "FILES-TO-ADD.md").write_text(
        "# Files to add\n\n", encoding="utf-8"
    )
    (patch / "FILES-TO-REPLACE.md").write_text(
        "# Files to replace\n\n"
        "- `CLAUDE-DIRECTORY/agents/existing.md`\n",
        encoding="utf-8",
    )
    source.write_text("locally customized\n", encoding="utf-8")

    result = run(patch, installed)

    assert result.returncode == 1
    report = json.loads(
        (patch / "DEPLOY-PREFLIGHT-REPORT.json").read_text(encoding="utf-8")
    )
    check = next(
        item for item in report["checks"] if item["check"] == "installed-state"
    )
    assert check["passed"] is False
    assert "differs from declared base" in check["findings"][0]
