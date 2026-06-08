import shutil
from pathlib import Path

from rich.console import Console

from agikit.builders import initialize_tool_package, register_package_in_agent, remove_package_from_agent, remove_tool_package
from agikit.ui import build_note_panel, print_divider, print_error, print_section_header, print_step, print_success


def run_tool_init_command(console: Console, tool_name: str) -> int:
    project_root = Path.cwd()
    marker = project_root / ".agikit" / "project.json"

    if not marker.exists():
        print_error(console, "current directory is not an agikit project.")
        return 1

    if shutil.which("uv") is None:
        print_error(console, "`uv` is required to create tool packages.")
        return 1

    print_section_header(console, "agikit tool init", "Creating a new tool package")
    print_step(console, "Project root", str(project_root))
    print_step(console, "Selected tool", tool_name)
    print_step(console, "Package manager", "uv init")

    try:
        target_dir = initialize_tool_package(project_root=project_root, tool_name=tool_name)
        register_package_in_agent(project_root, tool_name)
    except (FileExistsError, RuntimeError) as exc:
        print_error(console, str(exc))
        return 1
    except Exception as exc:
        print_error(console, f"tool created but agent.yaml could not be updated: {exc}")
        return 1

    print_divider(console)
    console.print(
        build_note_panel(
            "Tool Ready",
            [
                f"[green]OK[/] Tool created at [bold]{target_dir}[/]",
                "Created plugin.py and manifest.json with a ready-to-edit starter tool.",
            ],
            console=console,
        )
    )
    print_success(console, f"Done! Installed 1 tool package: {tool_name}")
    return 0


def run_tool_remove_command(console: Console, tool_name: str) -> int:
    project_root = Path.cwd()
    marker = project_root / ".agikit" / "project.json"

    if not marker.exists():
        print_error(console, "current directory is not an agikit project.")
        return 1

    print_section_header(console, "agikit tool remove", "Removing a tool package")
    print_step(console, "Project root", str(project_root))
    print_step(console, "Selected tool", tool_name)

    try:
        removed_dir = remove_tool_package(project_root, tool_name)
        remove_package_from_agent(project_root, tool_name)
    except (FileNotFoundError, Exception) as exc:
        print_error(console, str(exc))
        return 1

    print_divider(console)
    console.print(
        build_note_panel(
            "Tool Removed",
            [
                f"[green]OK[/] Removed [bold]{removed_dir}[/]",
                "The package reference was also removed from agent.yaml.",
            ],
            console=console,
        )
    )
    print_success(console, f"Done! Removed tool package: {tool_name}")
    return 0
