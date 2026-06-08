from pathlib import Path

from rich.console import Console

from agikit.builders import initialize_skill
from agikit.ui import build_note_panel, print_divider, print_error, print_section_header, print_step, print_success


def run_skill_init_command(console: Console, skill_name: str) -> int:
    project_root = Path.cwd()
    marker = project_root / ".agikit" / "project.json"

    if not marker.exists():
        print_error(console, "current directory is not an agikit project.")
        return 1

    print_section_header(console, "agikit skill init", "Creating a new skill starter")
    print_step(console, "Project root", str(project_root))
    print_step(console, "Selected skill", skill_name)

    try:
        skill_dir, skill_file = initialize_skill(root=project_root, skill_name=skill_name)
    except FileExistsError as exc:
        print_error(console, str(exc))
        return 1

    print_divider(console)
    console.print(
        build_note_panel(
            "Skill Ready",
            [
                f"[green]OK[/] Skill created at [bold]{skill_dir}[/]",
                f"Starter instructions written to [bold]{skill_file}[/]",
            ],
            console=console,
        )
    )
    print_success(console, f"Done! Installed 1 skill starter: {skill_name}")
    return 0
