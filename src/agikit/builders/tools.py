import subprocess
from pathlib import Path


def build_tools_directory(root: Path) -> Path:
    tools_dir = root / "tools"
    tools_dir.mkdir(parents=True, exist_ok=True)
    return tools_dir


def initialize_tool_package(project_root: Path, tool_name: str) -> Path:
    tools_dir = project_root / "tools"
    tools_dir.mkdir(parents=True, exist_ok=True)

    target_dir = tools_dir / tool_name
    if target_dir.exists():
        raise FileExistsError(f"Tool '{tool_name}' already exists.")

    result = subprocess.run(
        ["uv", "init", "--package", tool_name],
        cwd=tools_dir,
        check=False,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip() or "Unknown uv error"
        raise RuntimeError(f"uv init failed: {stderr}")

    return target_dir
