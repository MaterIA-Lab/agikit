from pathlib import Path

from rich.console import Console

from agikit.builders import initialize_mcp
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
    except FileExistsError as exc:
        print_error(console, str(exc))
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
