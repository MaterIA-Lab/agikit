from pathlib import Path

from rich.console import Console

from agikit.builders import set_agent_type
from agikit.ui import build_note_panel, print_divider, print_error, print_section_header, print_step, print_success


def run_agent_type_command(console: Console, agent_type: str) -> int:
    project_root = Path.cwd()
    marker = project_root / ".agikit" / "project.json"
    if not marker.exists():
        print_error(console, "current directory is not an agikit project.")
        return 1

    print_section_header(console, "agikit agent type", "Updating the agent runtime type")
    print_step(console, "Project root", str(project_root))
    print_step(console, "Selected type", agent_type)

    try:
        agent_file = set_agent_type(project_root, agent_type)
    except Exception as exc:
        print_error(console, str(exc))
        return 1

    print_divider(console)
    console.print(
        build_note_panel(
            "Agent Updated",
            [
                f"[green]OK[/] Updated [bold]{agent_file}[/]",
                "The content block was regenerated to match the selected backend format.",
            ],
            console=console,
        )
    )
    print_success(console, f"Done! Agent type is now {agent_type}.")
    return 0
