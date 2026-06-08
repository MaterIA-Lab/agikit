from pathlib import Path


def _humanize_name(agent_name: str) -> str:
    return "".join(part.capitalize() for part in agent_name.replace("_", "-").split("-"))


def build_agent_config(root: Path, agent_name: str, agent_type: str = "multiskilled") -> Path:
    display_name = _humanize_name(agent_name)
    description = (
        "Describe the agent in one or two short lines.\n"
        "Explain its main goal and the type of tasks it should handle."
    )
    content = f"""name: {agent_name}
type: {agent_type}
metadata:
  display_name: {display_name}
  description: |
    {description.replace(chr(10), chr(10) + "    ")}
  tags:
    - generalist
  use_cases:
    - Answering questions across various domains.
    - Search the web for quick information retrieval.
  visuals:
    accent_color: "#9F8CFF"
    accent_color_secondary: "#DCEBFF"
    glow_color: "#8F7DFF"
    icon_url: ""
    uses_icon: false
  frontend_hints: []
config:
  model: gpt-4.1-nano
  max_iterations: 30
"""
    agent_file = root / "agent.yaml"
    agent_file.write_text(content, encoding="utf-8")
    return agent_file
