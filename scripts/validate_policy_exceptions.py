from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "exception_id",
    "policy_id",
    "scope",
    "reason",
    "owner",
    "expires_at",
    "compensating_controls",
    "status",
}
STATUSES = {"proposed", "approved", "rejected", "expired"}


def parse_expiration(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args()

    root = Path(args.root).resolve()
    exception_root = root / ".atlas" / "policy" / "exceptions"
    policy_ids = {
        json.loads(path.read_text(encoding="utf-8"))["policy_id"]
        for path in (root / "policies").glob("*.json")
    }
    failures: list[str] = []
    seen_ids: set[str] = set()
    paths = sorted(exception_root.glob("*.json")) if exception_root.exists() else []

    for path in paths:
        relative = path.relative_to(root).as_posix()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            failures.append(f"{relative}: invalid JSON: {exc}")
            continue

        missing = REQUIRED - data.keys()
        if missing:
            failures.append(f"{relative}: missing {', '.join(sorted(missing))}")
            continue
        if data["exception_id"] in seen_ids:
            failures.append(f"{relative}: duplicate exception_id")
        seen_ids.add(data["exception_id"])
        if data["policy_id"] not in policy_ids:
            failures.append(f"{relative}: unknown policy_id {data['policy_id']}")
        if data["status"] not in STATUSES:
            failures.append(f"{relative}: invalid status {data['status']}")
        for field in [
            "exception_id",
            "policy_id",
            "scope",
            "reason",
            "owner",
            "expires_at",
        ]:
            if not isinstance(data[field], str) or not data[field].strip():
                failures.append(f"{relative}: {field} must be a non-empty string")
        if not isinstance(data["compensating_controls"], list):
            failures.append(f"{relative}: compensating_controls must be an array")
        elif data["status"] == "approved" and not data["compensating_controls"]:
            failures.append(
                f"{relative}: approved exception needs compensating controls"
            )

        try:
            expiration = parse_expiration(data["expires_at"])
        except (TypeError, ValueError):
            failures.append(f"{relative}: invalid expires_at")
            continue
        if data["status"] == "approved" and expiration <= datetime.now(timezone.utc):
            failures.append(f"{relative}: approved exception is expired")

    if failures:
        print("Policy exception validation failed:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print(f"Policy exception validation passed: {len(paths)} records")


if __name__ == "__main__":
    main()
