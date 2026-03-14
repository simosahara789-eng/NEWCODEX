from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

from reverb_tool.client import ReverbAPIError, ReverbClient
from reverb_tool.endpoints import OPERATIONS


def _json_arg(value: str | None) -> dict[str, Any] | None:
    if value is None:
        return None
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("JSON must be an object")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reverbctl",
        description="Control Reverb API operations from CLI.",
    )
    parser.add_argument(
        "--token",
        default=os.getenv("REVERB_API_TOKEN"),
        help="Reverb API token. Defaults to REVERB_API_TOKEN env var.",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("REVERB_API_BASE_URL", "https://api.reverb.com/api"),
        help="API base URL.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-ops", help="List supported operations")

    call = subparsers.add_parser("call", help="Invoke an operation by name")
    call.add_argument("operation", choices=sorted(OPERATIONS.keys()))
    call.add_argument("--query", help="JSON object for query params")
    call.add_argument("--body", help="JSON object for request body")
    call.add_argument("--compact", action="store_true", help="Print compact JSON")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list-ops":
        print(json.dumps({k: vars(v) for k, v in OPERATIONS.items()}, indent=2))
        return

    if not args.token:
        print("Missing token. Use --token or REVERB_API_TOKEN", file=sys.stderr)
        raise SystemExit(2)

    op = OPERATIONS[args.operation]
    try:
        query = _json_arg(args.query)
        body = _json_arg(args.body)
    except (json.JSONDecodeError, ValueError) as err:
        print(f"Invalid JSON input: {err}", file=sys.stderr)
        raise SystemExit(2)

    client = ReverbClient(token=args.token, base_url=args.base_url)

    try:
        data = client.request(op.method, op.path, query=query, body=body)
    except ReverbAPIError as err:
        print(str(err), file=sys.stderr)
        raise SystemExit(1)

    if args.compact:
        print(json.dumps(data, separators=(",", ":")))
        return

    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
