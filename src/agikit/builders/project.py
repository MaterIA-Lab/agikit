from dataclasses import dataclass
from pathlib import Path

from .agent import build_agent_config
from .marker import build_agikit_marker
from .mcps import build_mcps_directory
from .prompt import build_prompt_file
from .skills import build_skills_directory
from .tools import build_tools_directory


@dataclass(slots=True)
class ScaffoldResult:
    root: Path
    prompt_file: Path
    skills_dir: Path
    mcps_dir: Path
    tools_dir: Path
    agent_file: Path
    marker_file: Path


def scaffold_agent_project(destination: Path, agent_name: str, agent_type: str = "fastagent") -> ScaffoldResult:
    destination.mkdir(parents=True, exist_ok=False)

    prompt_file = build_prompt_file(destination)
    skills_dir = build_skills_directory(destination)
    mcps_dir = build_mcps_directory(destination)
    tools_dir = build_tools_directory(destination)
    agent_file = build_agent_config(destination, agent_name=agent_name, agent_type=agent_type)
    marker_file = build_agikit_marker(destination, agent_name=agent_name)

    return ScaffoldResult(
        root=destination,
        prompt_file=prompt_file,
        skills_dir=skills_dir,
        mcps_dir=mcps_dir,
        tools_dir=tools_dir,
        agent_file=agent_file,
        marker_file=marker_file,
    )
