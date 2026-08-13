#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = [
    "admin-operations-surface", "application-search-design", "audit-log-design",
    "cms-content-modeling", "data-import-export-workflow", "feature-flag-rollout",
    "file-upload-storage-design", "form-mutation-design", "notification-system-design",
    "rate-limit-abuse-control", "transactional-email-delivery",
]
WORKFLOWS = ["saas-from-brief-delivery", "site-from-brief-delivery"]
REVIEW = "full-stack-delivery-review"
AGENT_SKILLS = {
    "backend-engineer": ["form-mutation-design", "application-search-design", "data-import-export-workflow", "rate-limit-abuse-control", "audit-log-design", "admin-operations-surface"],
    "frontend-engineer": ["form-mutation-design", "file-upload-storage-design", "notification-system-design", "cms-content-modeling", "application-search-design"],
    "integration-engineer": ["transactional-email-delivery", "notification-system-design", "file-upload-storage-design"],
    "platform-engineer": ["file-upload-storage-design", "rate-limit-abuse-control", "feature-flag-rollout"],
    "data-engineer": ["application-search-design", "data-import-export-workflow", "audit-log-design"],
    "security-engineer": ["rate-limit-abuse-control", "audit-log-design", "admin-operations-surface"],
    "content-designer": ["cms-content-modeling"],
    "product-manager": ["feature-flag-rollout", "notification-system-design"],
    "solution-blueprint-engineer": SKILLS,
}
ROUTING_CASES = [
    ("p2-form-mutation", "Design this edit form mutation for server validation authorization duplicate submit optimistic UI conflict and error recovery.", "form-mutation-design"),
    ("p2-file-upload", "Design private tenant file uploads with signed access size type validation object keys processing cleanup and cross-tenant denial.", "file-upload-storage-design"),
    ("p2-email", "Design verification and receipt email delivery with authoritative triggers idempotent retries suppression bounce handling and safe non-production recipients.", "transactional-email-delivery"),
    ("p2-notifications", "Design an in-app and email notification center with recipient rules preferences unread state deduplication fan-out quiet hours and retries.", "notification-system-design"),
    ("p2-rate-limit", "Protect OTP uploads AI generation and expensive APIs with actor-aware rate concurrency payload and provider spend limits.", "rate-limit-abuse-control"),
    ("p2-search", "Design tenant-scoped product search with full-text ranking filters stable pagination indexes freshness zero results and relevance evaluation.", "application-search-design"),
    ("p2-cms", "Model CMS content types drafts preview localization media slugs publishing lifecycle SEO fields and frontend rendering contracts.", "cms-content-modeling"),
    ("p2-audit", "Design audit records for privileged actions with actor tenant resource result correlation retention tamper expectations and safe investigation queries.", "audit-log-design"),
    ("p2-admin", "Design an internal support console with least privilege tenant context impersonation dangerous confirmations break-glass controls and audited actions.", "admin-operations-surface"),
    ("p2-feature-flag", "Plan a percentage and tenant feature rollout with trusted evaluation context safe defaults kill switch metrics rollback and flag cleanup.", "feature-flag-rollout"),
    ("p2-import-export", "Design a large CSV import and export workflow with mapping preview row validation partial errors idempotent background processing progress and secure artifacts.", "data-import-export-workflow"),
]


def update_registry() -> None:
    path = ROOT / ".claude" / "registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["skills"] = sorted(set(data.get("skills", [])) | set(SKILLS))
    data["workflows"] = sorted(set(data.get("workflows", [])) | set(WORKFLOWS))
    data["reviews"] = sorted(set(data.get("reviews", [])) | {REVIEW})
    assurance = data.setdefault("assurance", {})
    assurance["full_stack_delivery_model"] = "framework/full-stack-delivery-model.md"
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_validate_all() -> None:
    path = ROOT / "scripts" / "validate_all.py"
    text = path.read_text(encoding="utf-8")
    if "full-stack-delivery-pack" in text:
        return
    marker = '''        _python_step(
            root,
            "production-product-quality-pack",
            "Validate P1 production and product quality capability pack",
            "validate_production_product_quality_pack.py",
        ),
'''
    addition = marker + '''        _python_step(
            root,
            "full-stack-delivery-pack",
            "Validate P2 full-stack delivery capability pack",
            "validate_full_stack_delivery_pack.py",
        ),
'''
    if marker not in text:
        raise SystemExit("validate_all insertion marker not found")
    path.write_text(text.replace(marker, addition, 1), encoding="utf-8")


def update_agents() -> None:
    for agent, skills in AGENT_SKILLS.items():
        path = ROOT / ".claude" / "agents" / f"{agent}.md"
        text = path.read_text(encoding="utf-8")
        heading = "## P2 Full-Stack Delivery"
        if heading in text:
            continue
        block = "\n\n" + heading + "\n\nRoute applicable construction work through: " + ", ".join(f"`{name}`" for name in skills) + ". Preserve `framework/full-stack-delivery-model.md`, inherited Frontend Craft, and existing trust/assurance gates.\n"
        path.write_text(text.rstrip() + block, encoding="utf-8")


def update_routing_cases() -> None:
    path = ROOT / "tests" / "fixtures" / "capability-routing-cases.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    cases = data.setdefault("cases", [])
    ids = {case.get("id") for case in cases if isinstance(case, dict)}
    for case_id, query, expected in ROUTING_CASES:
        if case_id not in ids:
            cases.append({"id": case_id, "query": query, "expected": expected})
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def update_readme() -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("| Skills | 117 |", "| Skills | 128 |")
    text = text.replace("| Workflows | 81 |", "| Workflows | 83 |")
    text = text.replace("| Reviews | 73 |", "| Reviews | 74 |")
    text = text.replace("all 117 descriptions", "all 128 descriptions")
    text = text.replace("for all 117 descriptions", "for all 128 descriptions")
    if "## Full-Stack Delivery P2" not in text:
        section = '''\n## Full-Stack Delivery P2\n\nATLAS now composes reusable production primitives for building complete websites and SaaS products from a brief, rather than stopping at architecture and review.\n\nThe canonical model is `framework/full-stack-delivery-model.md`. Public sites use `site-from-brief-delivery`; authenticated systems use `saas-from-brief-delivery`. Eleven new skills cover form mutations, file/object storage, transactional email, notifications, abuse/resource limits, application search, CMS modeling, audit logs, privileged admin operations, feature rollout, and bulk import/export.\n\nSix focused blueprints cover premium marketing, content, subscription SaaS, internal admin, marketplace/ecommerce, and AI SaaS. Every user-facing blueprint inherits Frontend Craft, so P2 expands construction power without weakening the premium frontend standard.\n\n'''
        text = text.replace("## Discovery descriptions and hover surfaces", section + "## Discovery descriptions and hover surfaces", 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    update_registry()
    update_validate_all()
    update_agents()
    update_routing_cases()
    update_readme()
    print("P2 source integration applied")


if __name__ == "__main__":
    main()
