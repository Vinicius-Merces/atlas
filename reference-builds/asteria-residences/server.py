#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import secrets
import threading
import time
from collections import defaultdict, deque
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
DATA = Path(os.environ.get("ASTERIA_DATA_DIR", str(ROOT / "data")))
DATA.mkdir(parents=True, exist_ok=True)
LEADS = DATA / "leads.jsonl"
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ALLOWED = {"Solis", "Atrium", "Garden", "Not sure"}
RATE: dict[str, deque[float]] = defaultdict(deque)
LOCK = threading.Lock()


def validate(body: dict[str, object]) -> dict[str, str]:
    errors: dict[str, str] = {}
    name = str(body.get("name", "")).strip()
    email = str(body.get("email", "")).strip()
    phone = str(body.get("phone", "")).strip()
    interest = str(body.get("interest", "")).strip()
    key = str(body.get("idempotency_key", "")).strip()
    if not 2 <= len(name) <= 80:
        errors["name"] = "Use 2-80 characters."
    if len(email) > 120 or not EMAIL.match(email):
        errors["email"] = "Use a valid email address."
    if not 8 <= len(phone) <= 25:
        errors["phone"] = "Use 8-25 characters."
    if interest not in ALLOWED:
        errors["interest"] = "Choose a listed residence."
    if body.get("consent") is not True:
        errors["consent"] = "Consent is required."
    if not 16 <= len(key) <= 128:
        errors["idempotency_key"] = "A valid idempotency key is required."
    return errors


def existing(key: str) -> dict[str, object] | None:
    if not LEADS.exists():
        return None
    for line in reversed(LEADS.read_text(encoding="utf-8").splitlines()):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("idempotency_key") == key:
            return row
    return None


class Handler(SimpleHTTPRequestHandler):
    server_version = "AsteriaReference/1.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)

    def send_json(self, status: int, payload: dict[str, object]) -> None:
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        if urlparse(self.path).path == "/api/health":
            self.send_json(200, {"status": "ok", "service": "asteria-reference"})
            return
        super().do_GET()

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/leads":
            self.send_json(404, {"message": "Not found"})
            return
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length > 16384:
            self.send_json(413, {"message": "Payload too large"})
            return
        ip = self.client_address[0]
        now = time.time()
        with LOCK:
            queue = RATE[ip]
            while queue and now - queue[0] > 60:
                queue.popleft()
            if len(queue) >= 5:
                self.send_json(429, {"message": "Too many requests. Please try again shortly."})
                return
            queue.append(now)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self.send_json(400, {"message": "Invalid JSON"})
            return
        errors = validate(body)
        if errors:
            self.send_json(422, {"message": "Please review the form.", "errors": errors})
            return
        key = str(body["idempotency_key"])
        prior = existing(key)
        if prior:
            self.send_json(200, {"status": "accepted", "lead_id": prior["lead_id"], "duplicate": True, "persisted": True})
            return
        if os.environ.get("ASTERIA_ENABLE_TEST_FAILURES") == "1" and self.headers.get("X-Asteria-Test-Mode") == "provider-failure":
            self.send_json(503, {"message": "Visit service temporarily unavailable."})
            return
        row = {
            "lead_id": "lead_" + secrets.token_hex(8),
            "idempotency_key": key,
            "name": str(body["name"]).strip(),
            "email": str(body["email"]).strip(),
            "phone": str(body["phone"]).strip(),
            "interest": body["interest"],
            "consent": True,
            "accepted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        with LOCK:
            with LEADS.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, separators=(",", ":")) + "\n")
        self.send_json(201, {"status": "accepted", "lead_id": row["lead_id"], "duplicate": False, "persisted": True})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Asteria reference server on http://127.0.0.1:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
