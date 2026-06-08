import argparse
import shutil
from collections.abc import Sequence

from rich.console import Console

from agikit.commands import (
    run_build_command,
    run_init_command,
    run_mcp_init_command,
    run_skill_init_command,
    run_tool_init_command,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agikit",
        description="Scaffold and manage .agi agent projects.",
    )
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Create a new .agi template project.")
    init_parser.add_argument("name", help="Agent project directory name.")
    init_parser.add_argument(
        "--type",
        dest="agent_type",
        default="multiskilled",
        choices=("multiskilled", "fastagent"),
        help="Agent type written to agent.yaml.",
    )

    tool_parser = subparsers.add_parser("tool", help="Manage tool packages inside an agikit project.")
    tool_subparsers = tool_parser.add_subparsers(dest="tool_command")

    tool_init_parser = tool_subparsers.add_parser("init", help="Create a new tool package with uv.")
    tool_init_parser.add_argument("name", help="Tool package name.")

    skill_parser = subparsers.add_parser("skill", help="Manage skills inside an agikit project.")
    skill_subparsers = skill_parser.add_subparsers(dest="skill_command")

    skill_init_parser = skill_subparsers.add_parser("init", help="Create a new skill folder.")
    skill_init_parser.add_argument("name", help="Skill folder name.")

    mcp_parser = subparsers.add_parser("mcp", help="Manage MCP definitions inside an agikit project.")
    mcp_subparsers = mcp_parser.add_subparsers(dest="mcp_command")

    mcp_init_parser = mcp_subparsers.add_parser("init", help="Create a new MCP folder and JSON file.")
    mcp_init_parser.add_argument("name", help="MCP folder name.")

    subparsers.add_parser("build", help="Build the current template into a .agi archive.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    console = Console(highlight=False)
    parser = _build_parser()
    args = parser.parse_args(argv)

    if shutil.which("uv") is None:
        console.print("[bold red]Error:[/] agikit requires `uv` to be installed and available in PATH.")
        return 1

    if args.command == "init":
        return run_init_command(console=console, agent_name=args.name, agent_type=args.agent_type)
    if args.command == "tool" and args.tool_command == "init":
        return run_tool_init_command(console=console, tool_name=args.name)
    if args.command == "skill" and args.skill_command == "init":
        return run_skill_init_command(console=console, skill_name=args.name)
    if args.command == "mcp" and args.mcp_command == "init":
        return run_mcp_init_command(console=console, mcp_name=args.name)
    if args.command == "build":
        return run_build_command(console=console)

    parser.print_help()
    return 0
