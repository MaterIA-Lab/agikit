from pathlib import Path


DEFAULT_MCP = """{{
  "mcpServers": {{
    "{server_name}": {{
      "command": "your-command-to-start-the-server",
      "args": ["--arg1", "--arg2"]
    }}
  }},
  "metadata": {{
    "pkg_ui_metadata": {{
      "display_name": "{display_name}",
      "categories": [
        "your-category"
      ],
      "description": "Add a brief description of your package here.",
      "uses_icon": false,
      "icon_url": ""
    }}
  }}
}}
"""


def build_mcps_directory(root: Path) -> Path:
    mcps_dir = root / "mcps"
    mcps_dir.mkdir(parents=True, exist_ok=True)
    return mcps_dir


def initialize_mcp(root: Path, mcp_name: str) -> tuple[Path, Path]:
    mcps_dir = root / "mcps"
    mcps_dir.mkdir(parents=True, exist_ok=True)

    mcp_dir = mcps_dir / mcp_name
    if mcp_dir.exists():
        raise FileExistsError(f"MCP '{mcp_name}' already exists.")

    mcp_dir.mkdir(parents=True, exist_ok=False)
    mcp_file = mcp_dir / f"{mcp_name}.json"
    mcp_file.write_text(
        DEFAULT_MCP.format(server_name=mcp_name, display_name=mcp_name),
        encoding="utf-8",
    )
    return mcp_dir, mcp_file
