#!/usr/bin/env python3
"""Validate the ATLAS Frontend Craft capability pack."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"
OVERLAY = ROOT / "framework" / "capabilities" / "frontend-craft.yaml"
MODEL = ROOT / "framework" / "frontend-craft-model.md"
WORKFLOW = ROOT / ".claude" / "workflows" / "frontend-feature-delivery.md"
REVIEW = ROOT / ".claude" / "reviews" / "frontend-craft-review.md"
MEMORY = ROOT / ".claude" / "memory" / "capabilities" / "frontend-craft.md"

REQUIRED_SKILLS = {
    "frontend-stack-selection",
    "interface-visual-direction",
    "motion-choreography",
    "immersive-3d-experience",
    "responsive-layout-audit",
    "visual-regression-review",
    "frontend-craft-review",
    "web-performance-field-readiness",
}

REQUIRED_AGENTS = {
    "frontend-engineer": {
        "framework/frontend-craft-model.md",
        "frontend-stack-selection",
        "motion-choreography",
        "responsive-layout-audit",
        "frontend-craft-review",
    },
    "ux-director": {
        "framework/frontend-craft-model.md",
        "interface-visual-direction",
        "frontend-craft-review",
    },
    "design-system-engineer": {
        "framework/frontend-craft-model.md",
        "design-token-architecture",
        "component-reuse-assessment",
    },
}


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
    try:
        raw, _ = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError(
            f"unterminated YAML frontmatter: {path.relative_to(ROOT)}"
        ) from exc
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError(f"invalid YAML frontmatter: {path.relative_to(ROOT)}")
    return data


def main() -> None:
    failures: list[str] = []

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registered_skills = set(registry.get("skills", []))
    registered_workflows = set(registry.get("workflows", []))
    registered_reviews = set(registry.get("reviews", []))

    missing_registry_skills = sorted(REQUIRED_SKILLS - registered_skills)
    if missing_registry_skills:
        failures.append(
            "frontend craft skills missing from registry: "
            + ", ".join(missing_registry_skills)
        )

    if "frontend-feature-delivery" not in registered_workflows:
        failures.append("frontend-feature-delivery workflow is not registered")
    if "frontend-craft-review" not in registered_reviews:
        failures.append("frontend-craft-review gate is not registered")

    experience = registry.get("experience", {})
    if not isinstance(experience, dict) or experience.get("frontend_craft_model") != (
        "framework/frontend-craft-model.md"
    ):
        failures.append("registry experience.frontend_craft_model is missing or invalid")

    required_files = [MODEL, OVERLAY, WORKFLOW, REVIEW, MEMORY]
    for path in required_files:
        if not path.is_file():
            failures.append(f"missing frontend craft artifact: {path.relative_to(ROOT)}")

    overlay: dict[str, object] = {}
    if OVERLAY.is_file():
        loaded = yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            overlay = loaded
        else:
            failures.append("frontend craft capability overlay must be a YAML mapping")

    overlay_skills = overlay.get("skills", [])
    if not isinstance(overlay_skills, list) or set(overlay_skills) != REQUIRED_SKILLS:
        failures.append("frontend craft overlay skills do not match the required skill set")
    if overlay.get("canonical_model") != "framework/frontend-craft-model.md":
        failures.append("frontend craft overlay canonical_model is invalid")
    if overlay.get("preferred_workflow") != "frontend-feature-delivery":
        failures.append("frontend craft overlay preferred_workflow is invalid")
    if overlay.get("required_review") != "frontend-craft-review":
        failures.append("frontend craft overlay required_review is invalid")

    for name in sorted(REQUIRED_SKILLS):
        canonical = ROOT / ".claude" / "skills" / name / "SKILL.md"
        wrapper = ROOT / ".agents" / "skills" / name / "SKILL.md"
        if not canonical.is_file():
            failures.append(f"missing canonical frontend craft skill: {name}")
            continue
        try:
            metadata = frontmatter(canonical)
        except ValueError as exc:
            failures.append(str(exc))
            continue
        if metadata.get("name") != name:
            failures.append(f"frontend craft skill {name} declares the wrong name")
        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            failures.append(f"frontend craft skill {name} has no discovery description")
        if not wrapper.is_file():
            failures.append(f"missing Codex-native frontend craft wrapper: {name}")
        else:
            wrapper_text = wrapper.read_text(encoding="utf-8")
            canonical_ref = f".claude/skills/{name}/SKILL.md"
            if canonical_ref not in wrapper_text:
                failures.append(
                    f"Codex wrapper {name} does not reference canonical skill {canonical_ref}"
                )

    for agent, required_terms in REQUIRED_AGENTS.items():
        path = ROOT / ".claude" / "agents" / f"{agent}.md"
        if not path.is_file():
            failures.append(f"missing frontend craft agent: {agent}")
            continue
        text = path.read_text(encoding="utf-8")
        missing_terms = sorted(term for term in required_terms if term not in text)
        if missing_terms:
            failures.append(
                f"agent {agent} is missing frontend craft references: "
                + ", ".join(missing_terms)
            )

    if WORKFLOW.is_file():
        workflow_text = WORKFLOW.read_text(encoding="utf-8")
        for name in sorted(REQUIRED_SKILLS):
            if name not in workflow_text:
                failures.append(f"frontend workflow does not reference required skill: {name}")

    if MODEL.is_file():
        model_text = MODEL.read_text(encoding="utf-8")
        technology_markers = [
            "Motion",
            "GSAP",
            "ScrollTrigger",
            "React Three Fiber",
            "prefers-reduced-motion",
            "visual-regression",
        ]
        for marker in technology_markers:
            if marker not in model_text:
                failures.append(f"frontend craft model is missing required marker: {marker}")

    if failures:
        print("Frontend craft pack validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(
        "Frontend craft pack valid: "
        f"{len(REQUIRED_SKILLS)} skills, 1 workflow, 1 independent review gate"
    )


if __name__ == "__main__":
    main()
