from pathlib import Path

from rich.console import Console
from agikit.ui import build_note_panel, print_divider, print_error, print_section_header, print_step, print_success


def run_build_command(console: Console) -> int:
    marker = Path.cwd() / ".agikit" / "project.json"
    if not marker.exists():
        print_error(console, "current directory is not an agikit project.")
        return 1

    print_section_header(console, "agikit build", "Inspecting current project build status")
    print_step(console, "Project root", str(Path.cwd()))
    print_divider(console)
    console.print(
        build_note_panel(
            "Build Status",
            [
                "[yellow]NOTE[/] Build support is still pending implementation.",
                "This command already validates that the current directory is an agikit project.",
                "Future releases can convert this template into a .agi archive.",
            ],
            border_style="yellow",
            console=console,
        )
    )
    print_success(console, "Done! Build scaffolding is recognized, archive output is not implemented yet.")
    return 0
