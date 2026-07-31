from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = json.loads(
    (ROOT / ".claude" / "registry.json").read_text(encoding="utf-8")
)


def test_every_registered_skill_has_native_runtime_entrypoints() -> None:
    for name in REGISTRY["skills"]:
        assert (ROOT / ".claude" / "skills" / name / "SKILL.md").is_file()
        assert (ROOT / ".agents" / "skills" / name / "SKILL.md").is_file()


def test_native_skill_wrappers_are_synchronized() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/sync_native_skills.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_codex_skill_map_uses_native_repository_skills() -> None:
    data = json.loads(
        (
            ROOT / "adapters" / "codex" / "generated" / "skill-map.json"
        ).read_text(encoding="utf-8")
    )
    assert len(data["entries"]) == len(REGISTRY["skills"])
    for entry in data["entries"]:
        assert entry["parity_type"] == "runtime-native"
        assert entry["status"] == "native"
        assert entry["adapter_path"] == (
            f".agents/skills/{entry['canonical_name']}/SKILL.md"
        )
