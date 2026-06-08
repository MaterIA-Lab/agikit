from pathlib import Path


DEFAULT_MCP = """{
  "name": "starter-mcp",
  "description": "Replace this MCP definition with your real server configuration.",
  "transport": {
    "type": "stdio",
    "command": "python",
    "args": [
      "-m",
      "starter_mcp"
    ]
  }
}
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
    mcp_file.write_text(DEFAULT_MCP.replace("starter-mcp", mcp_name), encoding="utf-8")
    return mcp_dir, mcp_file
