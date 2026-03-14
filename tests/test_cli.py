import json

from reverb_tool.cli import build_parser


def test_list_ops_command_parses() -> None:
    parser = build_parser()
    args = parser.parse_args(["list-ops"])
    assert args.command == "list-ops"


def test_call_command_parses() -> None:
    parser = build_parser()
    args = parser.parse_args(["call", "read_profile", "--query", json.dumps({"page": 1})])
    assert args.command == "call"
    assert args.operation == "read_profile"
