from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-root", required=True)
    parser.add_argument("--installed-root")
    args = parser.parse_args()

    patch = Path(args.patch_root)
    manifest = json.loads((patch / "PATCH-MANIFEST.json").read_text(encoding="utf-8"))
    checks = []

    if args.installed_root:
        installed = Path(args.installed_root)
        current = (installed / "VERSION").read_text(encoding="utf-8").strip()
        checks.append({
            "check": "base-version",
            "passed": current == manifest["from_version"],
            "expected": manifest["from_version"],
            "actual": current,
        })

    missing = []
    invalid_hash = []
    invalid_mapping = []
    for item in manifest["files"]:
        package_path = item.get("package_path", item["path"])
        path = patch / package_path
        if not path.is_file():
            missing.append(package_path)
            continue
        if sha256(path) != item["sha256"]:
            invalid_hash.append(package_path)
        target = item.get("target_path", item["path"])
        if target.startswith(".claude/") and not package_path.startswith("CLAUDE-DIRECTORY/"):
            invalid_mapping.append(package_path)

    checks.extend([
        {"check": "package-files", "passed": not missing, "findings": missing},
        {"check": "hashes", "passed": not invalid_hash, "findings": invalid_hash},
        {"check": "claude-directory-mapping", "passed": not invalid_mapping, "findings": invalid_mapping},
    ])

    outcome = "passed" if all(x["passed"] for x in checks) else "blocked"
    report = {
        "from_version": manifest["from_version"],
        "to_version": manifest["to_version"],
        "package": str(patch),
        "checks": checks,
        "outcome": outcome,
    }
    output = patch / "DEPLOY-PREFLIGHT-REPORT.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(output)
    if outcome == "blocked":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
