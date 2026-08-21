from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".claude" / "registry.json"
MEMORY = ROOT / ".claude" / "memory" / "capabilities" / "web-security-edge-assurance.md"

REQUIRED_FILES = [
    "framework/web-security-edge-assurance-model.md",
    "framework/capabilities/web-security-edge-assurance.yaml",
    ".claude/skills/web-security-header-audit/SKILL.md",
    ".claude/skills/crawler-edge-access-audit/SKILL.md",
    ".agents/skills/web-security-header-audit/SKILL.md",
    ".agents/skills/crawler-edge-access-audit/SKILL.md",
    ".claude/workflows/web-security-edge-assurance.md",
    ".claude/reviews/web-security-edge-assurance-review.md",
    ".claude/memory/capabilities/web-security-edge-assurance.md",
]


def require_text(path: str, terms: list[str]) -> None:
    text = (ROOT / path).read_text(encoding="utf-8").lower()
    missing = [term for term in terms if term.lower() not in text]
    if missing:
        raise SystemExit(f"{path}: missing required contract text: {missing}")


def main() -> None:
    missing_files = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing_files:
        raise SystemExit(f"Missing web security/edge pack files: {missing_files}")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    required_skills = {"web-security-header-audit", "crawler-edge-access-audit"}
    missing_skills = sorted(required_skills - set(registry.get("skills", [])))
    if missing_skills:
        raise SystemExit(f"Registry missing web security/edge skills: {missing_skills}")
    if "web-security-edge-assurance" not in set(registry.get("workflows", [])):
        raise SystemExit("Registry missing web-security-edge-assurance workflow")
    if "web-security-edge-assurance-review" not in set(registry.get("reviews", [])):
        raise SystemExit("Registry missing web-security-edge-assurance-review")
    assurance = registry.get("assurance", {})
    if not isinstance(assurance, dict) or assurance.get("web_security_edge_assurance_model") != "framework/web-security-edge-assurance-model.md":
        raise SystemExit("Registry assurance.web_security_edge_assurance_model is missing or invalid")

    overlay = yaml.safe_load(
        (ROOT / "framework/capabilities/web-security-edge-assurance.yaml").read_text(
            encoding="utf-8"
        )
    )
    if overlay.get("capability") != "web-security-edge-assurance":
        raise SystemExit("Capability overlay has the wrong capability id")
    if not required_skills.issubset(set(overlay.get("skills", []))):
        raise SystemExit("Capability overlay does not register both security-edge skills")

    owners = overlay.get("owners", {})
    owner_names: set[str] = set()
    if isinstance(owners, dict):
        for values in owners.values():
            if isinstance(values, list):
                owner_names.update(str(value) for value in values)
    registered_agents = set(registry.get("agents", []))
    unknown_owners = sorted(owner_names - registered_agents)
    if unknown_owners:
        raise SystemExit(f"Capability overlay references unknown agents: {unknown_owners}")

    require_text(
        "framework/web-security-edge-assurance-model.md",
        [
            "Content-Security-Policy",
            "sensitive public-path",
            "UA simulation",
            "HTTP 200",
            "blocked:csp",
            "Do not broadly allow all bots",
        ],
    )
    require_text(
        ".claude/skills/web-security-header-audit/SKILL.md",
        [
            "Content-Security-Policy-Report-Only",
            "'unsafe-inline'",
            "'unsafe-eval'",
            "blocked:csp",
            "rotation/revocation",
        ],
    )
    require_text(
        ".claude/skills/crawler-edge-access-audit/SKILL.md",
        [
            "UA simulation",
            "HTTP 200",
            "verified-bot",
            "Do not broadly allow all bots",
            "challenge/interstitial",
        ],
    )
    require_text(
        ".claude/reviews/web-security-edge-assurance-review.md",
        [
            "usable credential/private-key exposure",
            "broad security bypass",
            "proprietary crawler",
            "authoritative content",
        ],
    )
    require_text(
        ".claude/memory/capabilities/web-security-edge-assurance.md",
        [
            "configuration intent is not production evidence",
            "UA simulation",
            "CSP",
            "sensitive-path",
        ],
    )

    for skill in sorted(required_skills):
        canonical = (ROOT / f".claude/skills/{skill}/SKILL.md").read_text(encoding="utf-8")
        native = (ROOT / f".agents/skills/{skill}/SKILL.md").read_text(encoding="utf-8")
        for key in ("name:", "description:"):
            canonical_line = next(line for line in canonical.splitlines() if line.startswith(key))
            native_line = next(line for line in native.splitlines() if line.startswith(key))
            if canonical_line != native_line:
                raise SystemExit(f"{skill}: native discovery metadata drift for {key}")

    print("Web security and edge assurance pack valid: 2 skills, 1 workflow, 1 review")


if __name__ == "__main__":
    main()
