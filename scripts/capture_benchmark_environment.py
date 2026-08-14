#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def command_info(name: str) -> dict[str, object]:
    path = shutil.which(name)
    version: str | None = None
    if path:
        probes = ([path, "--version"], [path, "-V"])
        for probe in probes:
            try:
                completed = subprocess.run(probe, text=True, capture_output=True, timeout=5, check=False)
            except Exception:
                continue
            text = (completed.stdout or completed.stderr).strip().splitlines()
            if text:
                version = text[0][:240]
                break
    return {"available": bool(path), "path": path, "version": version}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Freeze benchmark runtime capabilities before implementation.")
    p.add_argument("--runtime", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--browser-source", choices=("runtime-native", "campaign-portable", "unavailable"), default="unavailable")
    p.add_argument("--portable-browser-eligible", action="store_true")
    p.add_argument("--deployment-native", action="store_true")
    p.add_argument("--campaign-deployment-adapter", action="store_true")
    p.add_argument("--network-mode", choices=("open", "allowlisted", "restricted", "unknown"), default="unknown")
    p.add_argument("--independent-review", action="store_true")
    p.add_argument("--notes", default="")
    return p


def main() -> int:
    args = parser().parse_args()
    commands = {name: command_info(name) for name in ("python", "python3", "node", "npm", "npx", "git", "chromium", "chromium-browser", "google-chrome")}
    native_browser = args.browser_source == "runtime-native"
    manifest = {
        "version": 1,
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "runtime": args.runtime,
        "model": args.model,
        "capabilities": {
            "browser": {
                "native_available": native_browser,
                "portable_fallback_eligible": bool(args.portable_browser_eligible),
                "source": args.browser_source,
                "details": "Host=" + platform.platform(),
            },
            "deployment": {
                "native_available": bool(args.deployment_native),
                "campaign_adapter_available": bool(args.campaign_deployment_adapter),
                "details": "Declared before implementation; availability must be proven again when used.",
            },
            "network": {"mode": args.network_mode, "details": "Runtime-declared network posture."},
            "independent_review": {"available": bool(args.independent_review), "details": "Separate reviewer availability frozen before implementation."},
            "commands": commands,
        },
        "notes": args.notes,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "runtime": args.runtime, "model": args.model, "browser_source": args.browser_source}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
