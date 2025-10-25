#!/usr/bin/env python3
"""
Lightweight HTTP server that (1) mints LiveKit access tokens for browser clients
and (2) serves the static frontend used to interact with the agent.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, urlparse

from dotenv import load_dotenv
from livekit import api

# Resolve important paths relative to this file so the script can be launched
# from the repository root or the AGENT directory.
AGENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = AGENT_DIR.parent
FRONTEND_DIR = REPO_ROOT / "frontend"


def _load_env() -> None:
    """Load environment variables required for token minting."""
    env_path_candidates = [
        AGENT_DIR / "keys.env",
        REPO_ROOT / "keys.env",
    ]

    for path in env_path_candidates:
        if path.exists():
            load_dotenv(path.as_posix())
            break


_load_env()

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
DEFAULT_ROOM = os.getenv("LIVEKIT_DEFAULT_ROOM", "galactactocus-room")


def _ensure_credentials() -> None:
    missing = [
        name
        for name, value in [
            ("LIVEKIT_URL", LIVEKIT_URL),
            ("LIVEKIT_API_KEY", LIVEKIT_API_KEY),
            ("LIVEKIT_API_SECRET", LIVEKIT_API_SECRET),
        ]
        if not value
    ]
    if missing:
        raise RuntimeError(
            "Missing LiveKit credentials: "
            + ", ".join(missing)
            + ". Please populate them in keys.env."
        )


from livekit.api import AccessToken  # from livekit-server-sdk
from livekit import api  # noqa: E402 - must be after _load_env()
from livekit.api import AccessToken, VideoGrants

def mint_access_token(identity: str, room: str) -> str:
    # LIVEKIT_API_KEY / LIVEKIT_API_SECRET must be set in your env or keys.env
    at = (
        AccessToken(os.getenv("LIVEKIT_API_KEY"), os.getenv("LIVEKIT_API_SECRET"))
        .with_identity(identity)             # required unique ID per participant
        .with_name(identity)                 # optional display name
        .with_grants(
            VideoGrants(
                room_join=True,
                room=room,
                can_publish=True,
                can_subscribe=True,
                # can_publish_data=True,   # enable if you plan to send data-only
            )
        )
        # .with_ttl(datetime.timedelta(hours=1))  # optional custom TTL
    )
    return at.to_jwt()



class TokenRequestHandler(SimpleHTTPRequestHandler):
    """Serve static frontend files and expose a /token endpoint."""

    def __init__(self, *args, directory: Optional[str] = None, **kwargs) -> None:
        super().__init__(*args, directory=directory or FRONTEND_DIR.as_posix(), **kwargs)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003 - upstream signature
        # Keep server output concise by routing through stderr.
        sys.stderr.write("%s - - %s\n" % (self.log_date_time_string(), format % args))

    # CORS helpers keep the token endpoint easy to consume during local dev.
    def _set_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        parsed = urlparse(self.path)
        if parsed.path == "/token":
            self.send_response(204)
            self._set_cors_headers()
            self.end_headers()
        else:
            super().do_OPTIONS()

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        parsed = urlparse(self.path)
        if parsed.path == "/token":
            self._handle_token_request(parsed.query)
            return

        # Fallback to the default static-file handling.
        super().do_GET()

    def _handle_token_request(self, query: str) -> None:
        params = parse_qs(query)
        identity = params.get("identity", [None])[0]
        room = params.get("room", [DEFAULT_ROOM])[0]

        if not identity:
            # Avoid token reuse collisions by defaulting to a semi-random identity.
            identity = f"web-{os.urandom(4).hex()}"

        try:
            token = mint_access_token(identity, room)
        except Exception as exc:  # pragma: no cover - defensive logging
            payload = json.dumps({"error": str(exc)})
            self.send_response(500)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload.encode("utf-8"))
            return

        payload = json.dumps(
            {
                "token": token,
                "url": LIVEKIT_URL,
                "identity": identity,
                "room": room,
            }
        )

        self.send_response(200)
        self._set_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload.encode("utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Serve frontend assets and mint LiveKit access tokens."
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host interface to bind (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port for the HTTP server (default: 8080)",
    )
    parser.add_argument(
        "--frontend-dir",
        type=Path,
        default=FRONTEND_DIR,
        help="Directory that contains the frontend assets.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.frontend_dir.exists():
        raise FileNotFoundError(
            f"Frontend directory '{args.frontend_dir}' not found. "
            "Create the frontend assets first."
        )

    handler_factory = lambda *h_args, **h_kwargs: TokenRequestHandler(  # noqa: E731
        *h_args,
        directory=args.frontend_dir.as_posix(),
        **h_kwargs,
    )

    server = HTTPServer((args.host, args.port), handler_factory)
    print(
        f"🔐 LiveKit token server running on http://{args.host}:{args.port}\n"
        f"   Serving static files from: {args.frontend_dir}\n"
        "   Request /token?identity=<name>&room=<room> to mint access tokens."
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down token server...")
        server.server_close()


if __name__ == "__main__":
    main()
