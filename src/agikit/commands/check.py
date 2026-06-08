from pathlib import Path

from rich.console import Console

from agikit.checks import collect_project_warnings
from agikit.ui import build_note_panel, print_divider, print_error, print_section_header, print_step, print_success


def run_check_command(console: Console) -> int:
    project_root = Path.cwd()
    marker = project_root / ".agikit" / "project.json"
    if not marker.exists():
        print_error(console, "current directory is not an agikit project.")
        return 1

    print_section_header(console, "agikit check", "Reviewing placeholder content and incomplete metadata")
    print_step(console, "Project root", str(project_root))

    warnings = collect_project_warnings(project_root)
    print_divider(console)

    if warnings:
        console.print(
            build_note_panel(
                "Warnings",
                [f"[yellow]WARN[/] {warning}" for warning in warnings],
                border_style="yellow",
                console=console,
            )
        )
        print_success(console, f"Check completed with {len(warnings)} warning(s).")
        return 1

    console.print(
        build_note_panel(
            "Check Result",
            ["[green]OK[/] No placeholder content was detected."],
            console=console,
        )
    )
    print_success(console, "Done! Project checks passed.")
    return 0
