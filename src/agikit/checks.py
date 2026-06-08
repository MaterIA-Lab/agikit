from __future__ import annotations

import json
from pathlib import Path

from agikit.builders import (
    DEFAULT_AGENT_DESCRIPTION,
    DEFAULT_MCP_UI_DESCRIPTION,
    DEFAULT_PACKAGE_SECTION_DESCRIPTION,
    DEFAULT_TOOL_MANIFEST_DESCRIPTION,
    load_agent_config,
)
from agikit.builders.prompt import DEFAULT_PROMPT
from agikit.builders.skills import DEFAULT_SKILL


def collect_project_warnings(project_root: Path) -> list[str]:
    warnings: list[str] = []

    warnings.extend(_check_agent_yaml(project_root))
    warnings.extend(_check_prompt(project_root))
    warnings.extend(_check_skills(project_root))
    warnings.extend(_check_tools(project_root))
    warnings.extend(_check_mcps(project_root))
    warnings.extend(_check_duplicate_package_names(project_root))

    return warnings


def _check_agent_yaml(project_root: Path) -> list[str]:
    warnings: list[str] = []
    agent_file = project_root / "agent.yaml"
    if not agent_file.exists():
        return ["Missing agent.yaml."]

    try:
        data = load_agent_config(agent_file)
    except Exception as exc:
        return [f"Could not parse agent.yaml: {exc}"]

    description = str(((data.get("metadata") or {}).get("description")) or "")
    if not description.strip() or description.strip() == DEFAULT_AGENT_DESCRIPTION:
        warnings.append("agent.yaml: fill metadata.description.")

    if str(data.get("type", "fastagent")) == "multiskilled":
        content = data.get("content") or {}
        for entry in content.get("toolkit", []):
            if not isinstance(entry, dict):
                continue
            name = str(entry.get("name", "unnamed"))
            if name == "shared":
                continue
            description = str(entry.get("description", ""))
            if not description.strip() or description.strip() == DEFAULT_PACKAGE_SECTION_DESCRIPTION:
                warnings.append(f"agent.yaml: fill content.toolkit description for package '{name}'.")

    return warnings


def _check_prompt(project_root: Path) -> list[str]:
    prompt_file = project_root / "prompt.md"
    if not prompt_file.exists():
        return ["Missing prompt.md."]
    content = prompt_file.read_text(encoding="utf-8")
    if content.strip() == DEFAULT_PROMPT.strip():
        return ["prompt.md still contains the default template."]
    return []


def _check_skills(project_root: Path) -> list[str]:
    warnings: list[str] = []
    skills_dir = project_root / "skills"
    if not skills_dir.exists():
        return warnings

    for skill_file in sorted(skills_dir.rglob("SKILL.md")):
        content = skill_file.read_text(encoding="utf-8")
        if content.strip() == DEFAULT_SKILL.strip():
            warnings.append(f"{skill_file.relative_to(project_root)} still contains the default skill template.")
    return warnings


def _check_tools(project_root: Path) -> list[str]:
    warnings: list[str] = []
    tools_dir = project_root / "tools"
    if not tools_dir.exists():
        return warnings

    for manifest_file in sorted(tools_dir.rglob("manifest.json")):
        try:
            data = json.loads(manifest_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            warnings.append(f"{manifest_file.relative_to(project_root)} is not valid JSON: {exc}")
            continue

        description = str(data.get("description", ""))
        if not description.strip() or description.strip() == DEFAULT_TOOL_MANIFEST_DESCRIPTION:
            warnings.append(f"{manifest_file.relative_to(project_root)}: fill description.")
    return warnings


def _check_mcps(project_root: Path) -> list[str]:
    warnings: list[str] = []
    mcps_dir = project_root / "mcps"
    if not mcps_dir.exists():
        return warnings

    for mcp_file in sorted(mcps_dir.rglob("*.json")):
        try:
            data = json.loads(mcp_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            warnings.append(f"{mcp_file.relative_to(project_root)} is not valid JSON: {exc}")
            continue

        metadata = data.get("metadata") or {}
        ui_metadata = metadata.get("pkg_ui_metadata") or {}
        description = str(ui_metadata.get("description", ""))
        if not description.strip() or description.strip() == DEFAULT_MCP_UI_DESCRIPTION:
            warnings.append(f"{mcp_file.relative_to(project_root)}: fill metadata.pkg_ui_metadata.description.")
    return warnings


def _check_duplicate_package_names(project_root: Path) -> list[str]:
    tools_dir = project_root / "tools"
    mcps_dir = project_root / "mcps"

    tool_names = {path.name for path in tools_dir.iterdir() if path.is_dir()} if tools_dir.exists() else set()
    mcp_names = {path.name for path in mcps_dir.iterdir() if path.is_dir()} if mcps_dir.exists() else set()

    duplicates = sorted(tool_names & mcp_names)
    return [f"name collision: '{name}' exists in both tools/ and mcps/." for name in duplicates]
