#!/usr/bin/env python3
"""HTTP server for the Cymbal Telecom Converged Commerce & Care Storefront (Local & Cloud Run)."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path

WEB_DIR = Path(__file__).resolve().parent
CONFIG_PATH = WEB_DIR / "deployment_config.json"


class CymbalConvergedHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def do_GET(self) -> None:
        if self.path.startswith("/api/config"):
            self._handle_config()
            return
        if self.path.startswith("/api/token"):
            self._handle_token()
            return
        if self.path.startswith("/healthz"):
            self._send_json(200, {"status": "ok"})
            return
        super().do_GET()

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_config(self) -> None:
        if CONFIG_PATH.exists():
            try:
                data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
                self._send_json(200, data)
                return
            except Exception as exc:
                self._send_json(500, {"error": str(exc)})
                return
        self._send_json(404, {"error": "deployment_config.json not found"})

    def _handle_token(self) -> None:
        try:
            import google.auth
            import google.auth.transport.requests

            credentials, _ = google.auth.default(
                scopes=["https://www.googleapis.com/auth/cloud-platform"]
            )
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)
            expiry = credentials.expiry or (
                datetime.now(timezone.utc) + timedelta(minutes=55)
            )
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            self._send_json(
                200,
                {
                    "accessToken": credentials.token,
                    "expiresAt": expiry.isoformat(),
                },
            )
        except Exception as exc:
            self._send_json(500, {"error": str(exc)})


def main() -> None:
    default_port = int(os.environ.get("PORT", "8081"))
    parser = argparse.ArgumentParser(description="Serve Cymbal Converged Storefront UI")
    parser.add_argument(
        "--port",
        type=int,
        default=default_port,
        help=f"Port to listen on (default: {default_port})",
    )
    args = parser.parse_args()

    server = ThreadingHTTPServer(("0.0.0.0", args.port), CymbalConvergedHandler)
    print(f"Serving Cymbal Converged Storefront UI at http://0.0.0.0:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
