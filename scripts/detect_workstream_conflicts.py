from __future__ import annotations
import argparse, json
from pathlib import PurePosixPath, Path

def overlaps(a: str, b: str) -> bool:
    pa, pb = PurePosixPath(a), PurePosixPath(b)
    return pa == pb or pa in pb.parents or pb in pa.parents

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    claims = manifest.get("claims", [])
    conflicts = []

    for i, left in enumerate(claims):
        for right in claims[i + 1:]:
            if left["workstream_id"] == right["workstream_id"]:
                continue
            if left["mode"] == "shared" and right["mode"] == "shared":
                continue
            for a in left["resources"]:
                for b in right["resources"]:
                    if overlaps(a, b):
                        conflicts.append({
                            "left_claim": left["claim_id"],
                            "right_claim": right["claim_id"],
                            "resource_left": a,
                            "resource_right": b,
                            "severity": "blocking",
                        })

    print(json.dumps({"conflicts": conflicts}, indent=2))
    if conflicts:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
