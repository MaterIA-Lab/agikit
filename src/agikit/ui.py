from __future__ import annotations

from rich import box
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


UNICODE_BANNER = r"""[bold #c792ea]
 █████╗  ██████╗ ██╗██╗  ██╗██╗████████╗
██╔══██╗██╔════╝ ██║██║ ██╔╝██║╚══██╔══╝
███████║██║  ███╗██║█████╔╝ ██║   ██║
██╔══██║██║   ██║██║██╔═██╗ ██║   ██║
██║  ██║╚██████╔╝██║██║  ██╗██║   ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝
[/]
"""

ASCII_BANNER = r"""[bold #c792ea]
  ___   ____ ___ _  ___ _____ _ _
 / _ | / ___|_ _| |/ (_)_   _(_) |
/ /_\\ || |  _ | || ' / _  | | | |/ __|
|  _  || |_| || || . \\ |  | | | |\\__ \\
\\_| |_/ \\____|___|_|\\_\\_|  |_| |_|___/
[/]
"""


def print_banner(console) -> None:
    console.print(UNICODE_BANNER if _supports_unicode(console) else ASCII_BANNER)


def print_command_header(console, label: str, subtitle: str | None = None) -> None:
    chars = _chars(console)
    print_banner(console)
    console.print(f"[bold #7dd3fc]{chars['top']}[/]   [bold white]{label}[/]")
    console.print(f"[bold #7dd3fc]{chars['pipe']}[/]")
    if subtitle:
        print_step(console, subtitle)
        console.print(f"[bold #7dd3fc]{chars['pipe']}[/]")


def print_section_header(console, label: str, subtitle: str | None = None) -> None:
    chars = _chars(console)
    console.print(f"[bold #7dd3fc]{chars['top']}[/]   [bold white]{label}[/]")
    console.print(f"[bold #7dd3fc]{chars['pipe']}[/]")
    if subtitle:
        print_step(console, subtitle)
        console.print(f"[bold #7dd3fc]{chars['pipe']}[/]")


def print_step(console, message: str, value: str | None = None) -> None:
    chars = _chars(console)
    console.print(f"[bold #7dd3fc]{chars['bullet']}[/]  [white]{message}[/]")
    if value:
        console.print(f"[bold #7dd3fc]{chars['pipe']}[/]  [dim]{value}[/]")


def print_info(console, message: str) -> None:
    chars = _chars(console)
    console.print(f"[bold #7dd3fc]{chars['pipe']}[/]  [dim]{message}[/]")


def print_success(console, message: str) -> None:
    chars = _chars(console)
    console.print(f"[bold #7dd3fc]{chars['pipe']}[/]")
    console.print(f"[bold #34d399]{chars['bottom']}[/]  [bold #34d399]{message}[/]")


def print_error(console, message: str) -> None:
    console.print(f"[bold red]Error:[/] {message}")


def build_summary_panel(title: str, rows: list[tuple[str, str]], console=None) -> Panel:
    table = Table.grid(expand=True)
    table.add_column(style="#f8fafc", ratio=1)
    table.add_column(style="#cbd5e1", ratio=3)
    for key, value in rows:
        table.add_row(f"[bold #fbbf24]{key}[/]", value)
    return Panel(
        table,
        title=f"[bold #7dd3fc]{title}[/]",
        border_style="#7dd3fc",
        padding=(1, 2),
        box=_panel_box(console),
    )


def build_note_panel(title: str, lines: list[str], border_style: str = "#34d399", console=None) -> Panel:
    content = Group(*[Text.from_markup(line) for line in lines])
    return Panel(
        content,
        title=f"[bold]{title}[/]",
        border_style=border_style,
        padding=(1, 2),
        box=_panel_box(console),
    )


def print_divider(console) -> None:
    chars = _chars(console)
    console.print(f"[bold #7dd3fc]{chars['pipe']}[/]")


def _supports_unicode(console) -> bool:
    encoding = getattr(console.file, "encoding", "") or ""
    return "utf" in encoding.lower()


def _chars(console) -> dict[str, str]:
    if _supports_unicode(console):
        return {"top": "┌", "pipe": "│", "bottom": "└", "bullet": "◇"}
    return {"top": "+", "pipe": "|", "bottom": "`", "bullet": "*"}


def _panel_box(console):
    if console is not None and not _supports_unicode(console):
        return box.ASCII
    return box.ROUNDED
