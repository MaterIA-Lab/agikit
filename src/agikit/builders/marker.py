from pathlib import Path


def build_agikit_marker(root: Path, agent_name: str) -> Path:
    marker_dir = root / ".agikit"
    marker_dir.mkdir(parents=True, exist_ok=True)

    marker_file = marker_dir / "project.json"
    marker_file.write_text(
        "{\n"
        f'  "name": "{agent_name}",\n'
        '  "format": "agi-template",\n'
        '  "version": 1,\n'
        '  "build": {\n'
        '    "status": "pending"\n'
        "  }\n"
        "}\n",
        encoding="utf-8",
    )
    return marker_file
