from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_context_builder_selects_route_sources_and_updates_envelope(
    tmp_path: Path,
) -> None:
    task = tmp_path / "task.json"
    task.write_text(
        json.dumps(
            {
                "id": "task-context",
                "task_type": "release",
                "summary": "Prepare a release",
                "risk": "high",
                "runtime": "codex",
                "primary_role": "release-manager",
                "supporting_roles": [],
                "workflow": "release-governance",
                "skills": ["release-integrity-verification"],
                "reviews": ["stability-review"],
                "validation": ["full-validation"],
                "affected_paths": ["release/STABLE-RELEASE-CHECKLIST.md"],
                "context_pack": "",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "context.md"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_context_pack.py",
            "--task-envelope",
            str(task),
            "--output",
            str(output),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    manifest = json.loads(
        output.with_suffix(".manifest.json").read_text(encoding="utf-8")
    )
    assert ".claude/agents/release-manager.md" in manifest["sources"]
    assert ".claude/workflows/release-governance.md" in manifest["sources"]
    assert (
        ".claude/skills/release-integrity-verification/SKILL.md"
        in manifest["sources"]
    )
    assert "adapters/codex/runtime-declaration.json" in manifest["sources"]
    assert manifest["source_hashes"]
    updated = json.loads(task.read_text(encoding="utf-8"))
    assert updated["context_pack"] == str(output)
    assert updated["context_manifest"] == str(
        output.with_suffix(".manifest.json")
    )
    assert updated["state"] == "context-ready"
