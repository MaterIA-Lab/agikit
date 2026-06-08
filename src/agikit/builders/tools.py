import json
import shutil
import subprocess
from pathlib import Path

DEFAULT_TOOL_MANIFEST_DESCRIPTION = (
    "Use this package when the agent needs project-specific tools, "
    "reusable actions, or integrations that are not covered by the core runtime."
)


PLUGIN_TEMPLATE = '''from typing import Callable

from agikit.types.tools import PackageMetadata, tool

# ============================================================
# Tool Definition
# ============================================================
#
# Tools are functions that can be executed by an agent.
#
# Requirements:
#
#   • The function must be decorated with @tool.
#
#   • A metadata dictionary must be provided to describe the tool for
#   the UI rendering.
#
#   • The function should include a clear and descriptive docstring
#     for the AI agents to understand when and how to use the tool.
#
# ============================================================

PACKAGE_UI_METADATA: PackageMetadata = {
    "display_name": "Test MCP",
    "categories": ["console"],
    "description": "A test MCP package for validating MCP integration and functionality.",
    "uses_icon": False,
    "icon_url": None,
}


@tool(
    metadata={
        "name": "say_hello_world",
        "display_name": "Say Hello World",
        "description": "A simple tool that says hello world.",
        "categories": ["console"],
        "uses_icon": False,
        "icon_url": None,
    }
)
def say_hello_world(input: str) -> str:
    """
    Say hello world and echo the input.

    Args:
        input: A string input to add after saying hello world.
    """
    print("Hello, world!")
    print(f"You said: {input}")

    return "Successfully said hello world."


def tools() -> list[Callable]:
    # Return all tools exposed by this package.
    #
    # Any tool included in the returned list will be available
    # for discovery and execution by the agent runtime.
    return [say_hello_world]
'''


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
        ["uv", "init", tool_name],
        cwd=tools_dir,
        check=False,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip() or "Unknown uv error"
        raise RuntimeError(f"uv init failed: {stderr}")

    _remove_nested_git_directory(target_dir)
    _replace_main_with_plugin(target_dir)
    _write_manifest(target_dir, tool_name)
    _ensure_agikit_dependency(target_dir)

    return target_dir


def remove_tool_package(project_root: Path, tool_name: str) -> Path:
    target_dir = project_root / "tools" / tool_name
    if not target_dir.exists():
        raise FileNotFoundError(f"Tool '{tool_name}' does not exist.")
    shutil.rmtree(target_dir)
    return target_dir


def _replace_main_with_plugin(target_dir: Path) -> None:
    main_file = target_dir / "main.py"
    if main_file.exists():
        main_file.unlink()

    plugin_file = target_dir / "plugin.py"
    plugin_file.write_text(PLUGIN_TEMPLATE, encoding="utf-8")


def _remove_nested_git_directory(target_dir: Path) -> None:
    git_dir = target_dir / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)


def _write_manifest(target_dir: Path, tool_name: str) -> None:
    manifest = {
        "name": tool_name,
        "version": "1.0.0",
        "description": DEFAULT_TOOL_MANIFEST_DESCRIPTION,
        "additional_installation": False,
        "installer_path": None,
    }
    manifest_path = target_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=4) + "\n", encoding="utf-8")


def _ensure_agikit_dependency(target_dir: Path) -> None:
    pyproject_path = target_dir / "pyproject.toml"
    content = pyproject_path.read_text(encoding="utf-8")

    content = content.replace(
        'description = "Add your description here"',
        'description = "Project-specific agikit tool package."',
        1,
    )
    content = content.replace("dependencies = []", 'dependencies = ["agikit"]', 1)

    pyproject_path.write_text(content, encoding="utf-8")
