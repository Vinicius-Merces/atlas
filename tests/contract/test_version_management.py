from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_current_version_surfaces_are_consistent() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/manage_version.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_update_preserves_historical_release_manifests(tmp_path: Path) -> None:
    sandbox = tmp_path / "atlas"
    config = json.loads(
        (ROOT / "release" / "version-sources.json").read_text(encoding="utf-8")
    )

    paths = {"VERSION", "release/version-sources.json"}
    paths.update(item["path"] for item in config["json_fields"])
    paths.update(item["path"] for item in config["line_fields"])
    for pattern in config["recursive_json_version_globs"]:
        paths.update(
            path.relative_to(ROOT).as_posix() for path in ROOT.glob(pattern)
        )
    paths.update(
        {
            "release/beta.9.manifest.json",
            "release/BETA-9-MIGRATION.md",
            "release/BETA-9-RELEASE-NOTES.md",
            "release/rc.1.manifest.json",
            "release/RC-1-MIGRATION.md",
            "release/RC-1-RELEASE-NOTES.md",
            "CHANGELOG.md",
        }
    )

    for relative in sorted(paths):
        source = ROOT / relative
        target = sandbox / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    old_manifest = (sandbox / "release/beta.9.manifest.json").read_bytes()
    old_migration = (sandbox / "release/BETA-9-MIGRATION.md").read_bytes()
    old_notes = (sandbox / "release/BETA-9-RELEASE-NOTES.md").read_bytes()
    old_rc_manifest = (sandbox / "release/rc.1.manifest.json").read_bytes()
    old_rc_migration = (sandbox / "release/RC-1-MIGRATION.md").read_bytes()
    old_rc_notes = (sandbox / "release/RC-1-RELEASE-NOTES.md").read_bytes()
    report = sandbox / "reports/update.json"
    target_version = "0.1.0-rc.2"

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "manage_version.py"),
            "--root",
            str(sandbox),
            "--set",
            target_version,
            "--report",
            str(report),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert (
        sandbox / "VERSION"
    ).read_text(encoding="utf-8").strip() == target_version
    assert (sandbox / "release/beta.9.manifest.json").read_bytes() == old_manifest
    assert (sandbox / "release/BETA-9-MIGRATION.md").read_bytes() == old_migration
    assert (sandbox / "release/BETA-9-RELEASE-NOTES.md").read_bytes() == old_notes
    assert (sandbox / "release/rc.1.manifest.json").read_bytes() == old_rc_manifest
    assert (sandbox / "release/RC-1-MIGRATION.md").read_bytes() == old_rc_migration
    assert (sandbox / "release/RC-1-RELEASE-NOTES.md").read_bytes() == old_rc_notes

    changed = json.loads(report.read_text(encoding="utf-8"))["changed_files"]
    assert "release/manifest.json" in changed
    assert "release/beta.9.manifest.json" not in changed
    assert "release/rc.1.manifest.json" not in changed
