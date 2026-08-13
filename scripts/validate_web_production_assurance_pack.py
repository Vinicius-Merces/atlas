#!/usr/bin/env python3
"""Validate the ATLAS Web Production Assurance capability pack."""

from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"
OVERLAY = ROOT / "framework" / "capabilities" / "web-production-assurance.yaml"
MODEL = ROOT / "framework" / "web-production-assurance-model.md"
WORKFLOW = ROOT / ".claude" / "workflows" / "web-production-assurance.md"
REVIEW = ROOT / ".claude" / "reviews" / "web-production-assurance-review.md"
MEMORY = ROOT / ".claude" / "memory" / "capabilities" / "web-production-assurance.md"

REQUIRED_SKILLS = {
    "browser-flow-validation",
    "seo-technical-audit",
    "structured-data-validation",
    "supply-chain-risk-audit",
}

REQUIRED_AGENTS = {
    "qa-engineer": {"framework/web-production-assurance-model.md", "browser-flow-validation", "seo-technical-audit"},
    "test-automation-engineer": {"framework/web-production-assurance-model.md", "browser-flow-validation"},
    "frontend-engineer": {"framework/web-production-assurance-model.md", "browser-flow-validation", "seo-technical-audit", "structured-data-validation"},
    "content-designer": {"framework/web-production-assurance-model.md", "seo-technical-audit", "structured-data-validation"},
    "security-engineer": {"framework/web-production-assurance-model.md", "supply-chain-risk-audit"},
    "dependency-manager": {"framework/web-production-assurance-model.md", "supply-chain-risk-audit"},
}


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing YAML frontmatter: {path.relative_to(ROOT)}")
    try:
        raw, _ = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError(f"unterminated YAML frontmatter: {path.relative_to(ROOT)}") from exc
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError(f"invalid YAML frontmatter: {path.relative_to(ROOT)}")
    return data


def main() -> None:
    failures: list[str] = []
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    missing = sorted(REQUIRED_SKILLS - set(registry.get("skills", [])))
    if missing:
        failures.append("web production assurance skills missing from registry: " + ", ".join(missing))
    if "web-production-assurance" not in set(registry.get("workflows", [])):
        failures.append("web-production-assurance workflow is not registered")
    if "web-production-assurance-review" not in set(registry.get("reviews", [])):
        failures.append("web-production-assurance-review gate is not registered")

    assurance = registry.get("assurance", {})
    if not isinstance(assurance, dict) or assurance.get("web_production_assurance_model") != "framework/web-production-assurance-model.md":
        failures.append("registry assurance.web_production_assurance_model is missing or invalid")

    for path in [MODEL, OVERLAY, WORKFLOW, REVIEW, MEMORY]:
        if not path.is_file():
            failures.append(f"missing web production assurance artifact: {path.relative_to(ROOT)}")

    overlay: dict[str, object] = {}
    if OVERLAY.is_file():
        loaded = yaml.safe_load(OVERLAY.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            overlay = loaded
        else:
            failures.append("web production assurance overlay must be a YAML mapping")

    if set(overlay.get("skills", [])) != REQUIRED_SKILLS:
        failures.append("web production assurance overlay skills do not match required skill set")
    if overlay.get("canonical_model") != "framework/web-production-assurance-model.md":
        failures.append("web production assurance overlay canonical_model is invalid")
    if overlay.get("preferred_workflow") != "web-production-assurance":
        failures.append("web production assurance overlay preferred_workflow is invalid")
    if overlay.get("required_review") != "web-production-assurance-review":
        failures.append("web production assurance overlay required_review is invalid")

    for name in sorted(REQUIRED_SKILLS):
        canonical = ROOT / ".claude" / "skills" / name / "SKILL.md"
        wrapper = ROOT / ".agents" / "skills" / name / "SKILL.md"
        if not canonical.is_file():
            failures.append(f"missing canonical web production skill: {name}")
            continue
        metadata = frontmatter(canonical)
        if metadata.get("name") != name:
            failures.append(f"web production skill {name} declares wrong name")
        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            failures.append(f"web production skill {name} has no discovery description")
        if not wrapper.is_file():
            failures.append(f"missing Codex-native web production wrapper: {name}")
        else:
            wrapper_text = wrapper.read_text(encoding="utf-8")
            if f".claude/skills/{name}/SKILL.md" not in wrapper_text:
                failures.append(f"Codex wrapper {name} does not reference canonical skill")
            wrapper_metadata = frontmatter(wrapper)
            if wrapper_metadata.get("description") != description:
                failures.append(f"Codex wrapper {name} discovery description drifted from canonical skill")

    for agent, required_terms in REQUIRED_AGENTS.items():
        path = ROOT / ".claude" / "agents" / f"{agent}.md"
        if not path.is_file():
            failures.append(f"missing web production assurance agent: {agent}")
            continue
        text = path.read_text(encoding="utf-8")
        missing_terms = sorted(term for term in required_terms if term not in text)
        if missing_terms:
            failures.append(f"agent {agent} is missing web production references: " + ", ".join(missing_terms))

    if WORKFLOW.is_file():
        text = WORKFLOW.read_text(encoding="utf-8")
        for name in sorted(REQUIRED_SKILLS):
            if name not in text:
                failures.append(f"web production workflow does not reference required skill: {name}")

    if MODEL.is_file():
        text = MODEL.read_text(encoding="utf-8").lower()
        markers = ["browser", "playwright", "canonical", "robots.txt", "sitemap", "structured data", "json-ld", "supply-chain", "dependency", "independent review"]
        for marker in markers:
            if marker not in text:
                failures.append(f"web production assurance model is missing required marker: {marker}")

    if failures:
        print("Web production assurance pack validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("Web production assurance pack valid: 4 skills, 1 workflow, 1 independent review gate")


if __name__ == "__main__":
    main()
