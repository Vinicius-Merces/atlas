from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "framework/web-security-edge-assurance-model.md",
    "framework/capabilities/web-security-edge-assurance.yaml",
    ".claude/skills/web-security-header-audit/SKILL.md",
    ".claude/skills/crawler-edge-access-audit/SKILL.md",
    ".agents/skills/web-security-header-audit/SKILL.md",
    ".agents/skills/crawler-edge-access-audit/SKILL.md",
    ".claude/workflows/web-security-edge-assurance.md",
    ".claude/reviews/web-security-edge-assurance-review.md",
]


def require_text(path: str, terms: list[str]) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    missing = [term for term in terms if term not in text]
    if missing:
        raise SystemExit(f"{path}: missing required contract text: {missing}")


def main() -> None:
    missing_files = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing_files:
        raise SystemExit(f"Missing web security/edge pack files: {missing_files}")

    overlay = yaml.safe_load(
        (ROOT / "framework/capabilities/web-security-edge-assurance.yaml").read_text(
            encoding="utf-8"
        )
    )
    if overlay.get("capability") != "web-security-edge-assurance":
        raise SystemExit("Capability overlay has the wrong capability id")
    required_skills = {"web-security-header-audit", "crawler-edge-access-audit"}
    if not required_skills.issubset(set(overlay.get("skills", []))):
        raise SystemExit("Capability overlay does not register both security-edge skills")

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
