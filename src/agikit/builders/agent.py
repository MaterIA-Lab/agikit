from __future__ import annotations

from pathlib import Path

import yaml


DEFAULT_AGENT_DESCRIPTION = (
    "Describe the agent in one or two short lines.\n"
    "Explain its main goal and the type of tasks it should handle."
)
DEFAULT_PACKAGE_SECTION_DESCRIPTION = "Explain here when should the agent use this tools"


def _humanize_name(agent_name: str) -> str:
    return "".join(part.capitalize() for part in agent_name.replace("_", "-").split("-"))


def build_agent_config(root: Path, agent_name: str, agent_type: str = "fastagent") -> Path:
    agent_file = root / "agent.yaml"
    content = {
        "name": agent_name,
        "type": agent_type,
        "metadata": {
            "display_name": _humanize_name(agent_name),
            "description": DEFAULT_AGENT_DESCRIPTION,
            "tags": ["generalist"],
            "use_cases": [
                "Answering questions across various domains.",
                "Search the web for quick information retrieval.",
            ],
            "visuals": {
                "accent_color": "#9F8CFF",
                "accent_color_secondary": "#DCEBFF",
                "glow_color": "#8F7DFF",
                "icon_url": "",
                "uses_icon": False,
            },
            "frontend_hints": [],
        },
        "content": _build_content(agent_type=agent_type, package_names=[]),
        "config": {
            "model": "gpt-4.1-nano",
            "max_iterations": 30,
        },
    }
    save_agent_config(agent_file, content)
    return agent_file


def load_agent_config(agent_file: Path) -> dict:
    data = yaml.safe_load(agent_file.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError("agent.yaml must contain a mapping at the top level")
    return data


def save_agent_config(agent_file: Path, content: dict) -> None:
    serialized = yaml.safe_dump(
        content,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=False,
        width=1000,
    )
    agent_file.write_text(serialized, encoding="utf-8")


def set_agent_type(root: Path, agent_type: str) -> Path:
    agent_file = root / "agent.yaml"
    data = load_agent_config(agent_file)
    package_names = extract_package_names(data)
    descriptions = extract_package_descriptions(data)
    data["type"] = agent_type
    data["content"] = _build_content(agent_type=agent_type, package_names=package_names, descriptions=descriptions)
    save_agent_config(agent_file, data)
    return agent_file


def register_package_in_agent(root: Path, package_name: str) -> Path:
    agent_file = root / "agent.yaml"
    data = load_agent_config(agent_file)
    package_names = extract_package_names(data)
    if package_name not in package_names:
        package_names.append(package_name)
    descriptions = extract_package_descriptions(data)
    agent_type = str(data.get("type", "fastagent"))
    data["content"] = _build_content(agent_type=agent_type, package_names=package_names, descriptions=descriptions)
    save_agent_config(agent_file, data)
    return agent_file


def remove_package_from_agent(root: Path, package_name: str) -> Path:
    agent_file = root / "agent.yaml"
    data = load_agent_config(agent_file)
    package_names = [name for name in extract_package_names(data) if name != package_name]
    descriptions = extract_package_descriptions(data)
    descriptions.pop(package_name, None)
    agent_type = str(data.get("type", "fastagent"))
    data["content"] = _build_content(agent_type=agent_type, package_names=package_names, descriptions=descriptions)
    save_agent_config(agent_file, data)
    return agent_file


def extract_package_names(data: dict) -> list[str]:
    content = data.get("content") or {}
    agent_type = str(data.get("type", "fastagent"))
    names: list[str] = []

    if agent_type == "multiskilled":
        for entry in content.get("toolkit", []):
            if not isinstance(entry, dict):
                continue
            tools = entry.get("tools", [])
            for tool in tools:
                if isinstance(tool, dict) and tool.get("type") == "package" and isinstance(tool.get("id"), str):
                    names.append(tool["id"])
                    break
    else:
        for entry in content.get("tools", []):
            if isinstance(entry, dict) and entry.get("type") == "package" and isinstance(entry.get("id"), str):
                names.append(entry["id"])

    deduped: list[str] = []
    for name in names:
        if name not in deduped:
            deduped.append(name)
    return deduped


def extract_package_descriptions(data: dict) -> dict[str, str]:
    descriptions: dict[str, str] = {}
    content = data.get("content") or {}
    for entry in content.get("toolkit", []):
        if not isinstance(entry, dict):
            continue
        tools = entry.get("tools", [])
        for tool in tools:
            if isinstance(tool, dict) and tool.get("type") == "package" and isinstance(tool.get("id"), str):
                descriptions[tool["id"]] = str(entry.get("description", DEFAULT_PACKAGE_SECTION_DESCRIPTION))
                break
    return descriptions


def _build_content(agent_type: str, package_names: list[str], descriptions: dict[str, str] | None = None) -> dict:
    descriptions = descriptions or {}
    if agent_type == "multiskilled":
        toolkit = [
            {
                "name": "shared",
                "description": "Shared actions",
                "tools": _shared_tools(),
            }
        ]
        for name in package_names:
            toolkit.append(
                {
                    "name": name,
                    "description": descriptions.get(name, DEFAULT_PACKAGE_SECTION_DESCRIPTION),
                    "tools": [
                        {
                            "type": "package",
                            "id": name,
                        }
                    ],
                }
            )
        return {"toolkit": toolkit}

    tools = _shared_tools()
    for name in package_names:
        tools.append(
            {
                "type": "package",
                "id": name,
            }
        )
    return {"tools": tools}


def _shared_tools() -> list[dict]:
    return [
        {
            "type": "tool",
            "id": "meta.reason",
        },
        {
            "type": "tool",
            "id": "meta.feedback",
            "config": {
                "language": "Spanish",
            },
        },
    ]
