from pathlib import Path


DEFAULT_SKILL = """# Default Skill

Use this folder for optional agent-specific skills.

Each skill can be a single folder with a `SKILL.md`, or a tree of nested skill folders.
Document:
- when the skill should be used
- what workflow it teaches
- any important caveats
"""


def build_skills_directory(root: Path) -> Path:
    skills_dir = root / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    return skills_dir


def initialize_skill(root: Path, skill_name: str) -> tuple[Path, Path]:
    skills_dir = root / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    skill_dir = skills_dir / skill_name
    if skill_dir.exists():
        raise FileExistsError(f"Skill '{skill_name}' already exists.")

    skill_dir.mkdir(parents=True, exist_ok=False)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(DEFAULT_SKILL, encoding="utf-8")
    return skill_dir, skill_file
