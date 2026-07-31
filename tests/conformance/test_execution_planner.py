from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_execution_plan_resolves_capabilities_and_states_execution_boundary(
    tmp_path: Path,
) -> None:
    context = tmp_path / "context.md"
    context.write_text("# Context\n", encoding="utf-8")
    task = tmp_path / "task.json"
    task.write_text(
        json.dumps(
            {
                "id": "task-plan",
                "task_type": "feature",
                "summary": "Plan a feature",
                "risk": "medium",
                "primary_role": "product-architect",
                "supporting_roles": ["qa-engineer"],
                "workflow": "feature-delivery",
                "skills": ["product-requirement-decomposition"],
                "reviews": ["architecture-review", "qa-review"],
                "validation": ["project-tests"],
                "acceptance_criteria": ["Behavior is covered"],
                "constraints": ["Preserve compatibility"],
                "affected_paths": ["src"],
                "context_pack": str(context),
            }
        )
        + "\n",
        encoding="utf-8",
    )
    output = tmp_path / "plan.json"

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_execution_plan.py",
            "--task-envelope",
            str(task),
            "--runtime",
            "codex",
            "--output",
            str(output),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    plan = json.loads(output.read_text(encoding="utf-8"))
    assert plan["execution_mode"] == "ai-or-human-interpreted"
    assert plan["requires_external_execution"] is True
    assert plan["context_available"] is True
    assert plan["capability_sources"]["workflow"] == (
        ".claude/workflows/feature-delivery.md"
    )
    assert plan["capability_sources"]["skills"] == [
        ".claude/skills/product-requirement-decomposition/SKILL.md"
    ]


def test_execution_plan_blocks_missing_context_by_default(tmp_path: Path) -> None:
    task = tmp_path / "task.json"
    task.write_text(
        json.dumps(
            {
                "id": "task-plan",
                "task_type": "bug",
                "summary": "Fix a bug",
                "primary_role": "qa-engineer",
                "workflow": "bug-fix",
                "reviews": ["qa-review"],
                "validation": ["tests"],
                "context_pack": "",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/build_execution_plan.py",
            "--task-envelope",
            str(task),
            "--runtime",
            "codex",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "build_context_pack.py first" in (result.stdout + result.stderr)
