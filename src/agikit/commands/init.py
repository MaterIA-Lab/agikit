from pathlib import Path

from rich.console import Console

from agikit.builders import scaffold_agent_project
from agikit.ui import build_note_panel, build_summary_panel, print_command_header, print_divider, print_error, print_info, print_step, print_success


def run_init_command(console: Console, agent_name: str, agent_type: str = "multiskilled") -> int:
    destination = Path.cwd() / agent_name
    if destination.exists():
        print_error(console, f"'{agent_name}' already exists.")
        return 1

    print_command_header(console, "agikit init", "Scaffolding a new .agi template project")
    print_step(console, "Target", str(destination))
    print_step(console, "Agent type", agent_type)
    print_step(console, "Creating project structure...")

    result = scaffold_agent_project(destination=destination, agent_name=agent_name, agent_type=agent_type)

    print_divider(console)
    console.print(
        build_summary_panel(
            "Project Summary",
            [
                ("root", str(result.root)),
                ("prompt", "prompt.md"),
                ("skills", "skills/"),
                ("mcps", "mcps/"),
                ("tools", "tools/"),
                ("config", "agent.yaml"),
                ("marker", ".agikit/project.json"),
            ],
            console=console,
        )
    )
    print_info(console, "Created empty skills/, mcps/, and tools/ directories")
    print_info(console, "Add content later with agikit skill init, agikit mcp init, or agikit tool init")
    print_divider(console)
    console.print(
        build_note_panel(
            "Next Steps",
            [
                f"[green]OK[/] Project created at [bold]{result.root}[/]",
                "1. Edit [bold]prompt.md[/]",
                "2. Update [bold]agent.yaml[/]",
                "3. Add a skill with [bold]agikit skill init <skill-name>[/]",
                "4. Add an MCP with [bold]agikit mcp init <mcp-name>[/]",
                "5. Create tools with [bold]agikit tool init <tool-name>[/]",
            ],
            console=console,
        )
    )
    print_success(console, "Done! Your agent scaffold is ready.")
    return 0
