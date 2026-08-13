#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"
OVERLAY = ROOT / "framework" / "capabilities" / "full-stack-delivery.yaml"
MODEL = ROOT / "framework" / "full-stack-delivery-model.md"
MEMORY = ROOT / ".claude" / "memory" / "capabilities" / "full-stack-delivery.md"
REVIEW = ROOT / ".claude" / "reviews" / "full-stack-delivery-review.md"
WORKFLOWS = {
    "site-from-brief-delivery": ROOT / ".claude" / "workflows" / "site-from-brief-delivery.md",
    "saas-from-brief-delivery": ROOT / ".claude" / "workflows" / "saas-from-brief-delivery.md",
}
GROUPS = {
    "state_and_data": {"form-mutation-design", "file-upload-storage-design", "application-search-design", "data-import-export-workflow"},
    "communication_and_operations": {"transactional-email-delivery", "notification-system-design", "audit-log-design", "admin-operations-surface"},
    "product_delivery_controls": {"rate-limit-abuse-control", "feature-flag-rollout", "cms-content-modeling"},
}
REQUIRED_SKILLS = set().union(*GROUPS.values())
BLUEPRINTS = {
    "premium-marketing-site", "content-site", "subscription-saas",
    "internal-admin-tool", "marketplace-ecommerce", "ai-saas",
}
HEADINGS = ["## Purpose", "## Trigger conditions", "## Inputs", "## Procedure", "## Outputs", "## Dependencies", "## Limitations", "## Validation"]


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing frontmatter: {path.relative_to(ROOT)}")
    raw, _ = text[4:].split("\n---\n", 1)
    value = yaml.safe_load(raw)
    if not isinstance(value, dict):
        raise ValueError(f"invalid frontmatter: {path.relative_to(ROOT)}")
    return value


def main() -> None:
    failures: list[str] = []
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if not REQUIRED_SKILLS <= set(registry.get("skills", [])):
        failures.append("P2 skills are not fully registered")
    if not set(WORKFLOWS) <= set(registry.get("workflows", [])):
        failures.append("P2 workflows are not fully registered")
    if "full-stack-delivery-review" not in set(registry.get("reviews", [])):
        failures.append("P2 independent review is not registered")
    assurance = registry.get("assurance", {})
    if not isinstance(assurance, dict) or assurance.get("full_stack_delivery_model") != "framework/full-stack-delivery-model.md":
        failures.append("registry assurance.full_stack_delivery_model is missing")
    for path in [OVERLAY, MODEL, MEMORY, REVIEW, *WORKFLOWS.values()]:
        if not path.is_file():
            failures.append(f"missing P2 artifact: {path.relative_to(ROOT)}")
    if OVERLAY.is_file():
        overlay = yaml.safe_load(OVERLAY.read_text(encoding="utf-8")) or {}
        groups = overlay.get("skills", {})
        if not isinstance(groups, dict):
            failures.append("P2 overlay skills must be grouped mapping")
        else:
            for group, expected in GROUPS.items():
                if set(groups.get(group, [])) != expected:
                    failures.append(f"P2 skill group drifted: {group}")
        if overlay.get("required_review") != "full-stack-delivery-review":
            failures.append("P2 required review drifted")
    for name in sorted(REQUIRED_SKILLS):
        canonical = ROOT / ".claude" / "skills" / name / "SKILL.md"
        wrapper = ROOT / ".agents" / "skills" / name / "SKILL.md"
        if not canonical.is_file():
            failures.append(f"missing canonical P2 skill: {name}")
            continue
        metadata = frontmatter(canonical)
        if metadata.get("name") != name or not str(metadata.get("description", "")).strip():
            failures.append(f"invalid P2 discovery metadata: {name}")
        text = canonical.read_text(encoding="utf-8")
        for heading in HEADINGS:
            if heading not in text:
                failures.append(f"P2 skill {name} missing {heading}")
        if not wrapper.is_file() or f".claude/skills/{name}/SKILL.md" not in wrapper.read_text(encoding="utf-8"):
            failures.append(f"P2 Codex wrapper missing canonical reference: {name}")
    for name, path in WORKFLOWS.items():
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            if name == "saas-from-brief-delivery":
                for skill in REQUIRED_SKILLS:
                    if skill not in text:
                        failures.append(f"SaaS workflow does not route P2 skill: {skill}")
    for blueprint in BLUEPRINTS:
        if not (ROOT / "blueprints" / blueprint / "README.md").is_file():
            failures.append(f"missing P2 blueprint: {blueprint}")
    if MODEL.is_file():
        model = MODEL.read_text(encoding="utf-8").lower()
        for marker in ["brief", "premium frontend", "mutation", "file", "search", "notification", "rate", "audit", "admin", "feature", "cms", "import", "independent review"]:
            if marker not in model:
                failures.append(f"P2 model missing marker: {marker}")
    if failures:
        print("Full-stack delivery pack validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("Full-stack delivery pack valid: 11 skills, 2 workflows, 6 blueprints, 1 independent review gate")


if __name__ == "__main__":
    main()
