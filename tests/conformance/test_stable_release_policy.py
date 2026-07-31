from __future__ import annotations

import json
from pathlib import Path

from scripts.evaluate_policies import stable_release_gate


def prepare(root: Path, *, include_current_validation: bool) -> None:
    version = "1.2.3"
    release = root / "release"
    release.mkdir()
    (root / "VERSION").write_text(version + "\n", encoding="utf-8")
    (root / "CHANGELOG.md").write_text(
        f"# Changelog\n\n## {version}\n",
        encoding="utf-8",
    )
    (release / "manifest.json").write_text(
        json.dumps({"version": version}),
        encoding="utf-8",
    )
    (release / "STABLE-RELEASE-CHECKLIST.md").write_text(
        (
            "# Checklist\n\n- [x] complete\n\n"
            + (
                f"- `release/{version}-VALIDATION.md`\n"
                if include_current_validation
                else ""
            )
        ),
        encoding="utf-8",
    )
    for suffix in (
        "MIGRATION.md",
        "RELEASE-NOTES.md",
        "VALIDATION.md",
    ):
        (release / f"{version}-{suffix}").write_text(
            "# Evidence\n",
            encoding="utf-8",
        )
    (release / f"{version}.manifest.json").write_text(
        json.dumps({"version": version}),
        encoding="utf-8",
    )


def test_stable_gate_requires_current_version_evidence(tmp_path: Path) -> None:
    prepare(tmp_path, include_current_validation=False)

    passed, _, findings = stable_release_gate(tmp_path)

    assert passed is False
    assert any("current validation" in finding for finding in findings)


def test_stable_gate_accepts_complete_current_version_evidence(
    tmp_path: Path,
) -> None:
    prepare(tmp_path, include_current_validation=True)

    passed, _, findings = stable_release_gate(tmp_path)

    assert passed is True
    assert findings == []
