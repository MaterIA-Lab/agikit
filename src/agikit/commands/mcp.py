from pathlib import Path

from rich.console import Console

from agikit.builders import initialize_mcp, register_package_in_agent, remove_mcp, remove_package_from_agent
from agikit.ui import build_note_panel, print_divider, print_error, print_section_header, print_step, print_success


def run_mcp_init_command(console: Console, mcp_name: str) -> int:
    project_root = Path.cwd()
    marker = project_root / ".agikit" / "project.json"

    if not marker.exists():
        print_error(console, "current directory is not an agikit project.")
        return 1

    print_section_header(console, "agikit mcp init", "Creating a new MCP definition")
    print_step(console, "Project root", str(project_root))
    print_step(console, "Selected MCP", mcp_name)

    try:
        mcp_dir, mcp_file = initialize_mcp(root=project_root, mcp_name=mcp_name)
        register_package_in_agent(project_root, mcp_name)
    except FileExistsError as exc:
        print_error(console, str(exc))
        return 1
    except Exception as exc:
        print_error(console, f"MCP created but agent.yaml could not be updated: {exc}")
        return 1

    print_divider(console)
    console.print(
        build_note_panel(
            "MCP Ready",
            [
                f"[green]OK[/] MCP created at [bold]{mcp_dir}[/]",
                f"Starter config written to [bold]{mcp_file}[/]",
            ],
            console=console,
        )
    )
    print_success(console, f"Done! Installed 1 MCP starter: {mcp_name}")
    return 0


def run_mcp_remove_command(console: Console, mcp_name: str) -> int:
    project_root = Path.cwd()
    marker = project_root / ".agikit" / "project.json"

    if not marker.exists():
        print_error(console, "current directory is not an agikit project.")
        return 1

    print_section_header(console, "agikit mcp remove", "Removing an MCP package")
    print_step(console, "Project root", str(project_root))
    print_step(console, "Selected MCP", mcp_name)

    try:
        removed_dir = remove_mcp(project_root, mcp_name)
        remove_package_from_agent(project_root, mcp_name)
    except (FileNotFoundError, Exception) as exc:
        print_error(console, str(exc))
        return 1

    print_divider(console)
    console.print(
        build_note_panel(
            "MCP Removed",
            [
                f"[green]OK[/] Removed [bold]{removed_dir}[/]",
                "The package reference was also removed from agent.yaml.",
            ],
            console=console,
        )
    )
    print_success(console, f"Done! Removed MCP package: {mcp_name}")
    return 0
