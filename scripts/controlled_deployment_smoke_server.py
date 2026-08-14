#!/usr/bin/env python3
from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


HTML = b"""<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>ATLAS controlled deployment smoke</title><meta name=\"robots\" content=\"noindex,nofollow\"></head><body><main><h1>ATLAS controlled deployment smoke</h1><p>Public HTTPS ingress is alive.</p></main></body></html>"""
ROBOTS = b"User-agent: *\nDisallow: /\n"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/healthz":
            body = b"ok\n"
            content_type = "text/plain; charset=utf-8"
            status = 200
        elif self.path == "/robots.txt":
            body = ROBOTS
            content_type = "text/plain; charset=utf-8"
            status = 200
        elif self.path == "/":
            body = HTML
            content_type = "text/html; charset=utf-8"
            status = 200
        else:
            body = b"not found\n"
            content_type = "text/plain; charset=utf-8"
            status = 404
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        print(format % args, flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"ATLAS controlled deployment smoke listening on 127.0.0.1:{args.port}", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
