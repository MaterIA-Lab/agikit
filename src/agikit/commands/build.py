import json
import zipfile
from pathlib import Path

from rich.console import Console
from agikit.ui import build_summary_panel, print_divider, print_error, print_section_header, print_step, print_success


def run_build_command(console: Console) -> int:
    project_root = Path.cwd()
    marker = project_root / ".agikit" / "project.json"
    if not marker.exists():
        print_error(console, "current directory is not an agikit project.")
        return 1

    try:
        project_name = _load_project_name(marker)
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print_error(console, f"could not read project metadata: {exc}")
        return 1

    dist_dir = project_root / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    archive_path = dist_dir / f"{project_name}.agi"

    included_paths = [
        project_root / "mcps",
        project_root / "skills",
        project_root / "tools",
        project_root / "agent.yaml",
        project_root / "prompt.md",
    ]

    missing_paths = [path.name for path in included_paths if not path.exists()]
    if missing_paths:
        print_error(console, f"project is missing required paths: {', '.join(missing_paths)}")
        return 1

    print_section_header(console, "agikit build", "Inspecting current project build status")
    print_step(console, "Project root", str(project_root))
    print_step(console, "Project name", project_name)
    print_step(console, "Output archive", str(archive_path))
    print_step(console, "Packaging", "mcps/, skills/, tools/, agent.yaml, prompt.md")

    _build_archive(project_root=project_root, archive_path=archive_path)

    print_divider(console)
    console.print(
        build_summary_panel(
            "Build Output",
            [
                ("archive", str(archive_path)),
                ("format", ".agi (zip archive)"),
                ("includes", "mcps/, skills/, tools/, agent.yaml, prompt.md"),
            ],
            console=console,
        )
    )
    print_success(console, f"Done! Built {archive_path.name} in dist/.")
    return 0


def _load_project_name(marker_path: Path) -> str:
    data = json.loads(marker_path.read_text(encoding="utf-8"))
    name = data["name"]
    if not isinstance(name, str) or not name.strip():
        raise TypeError("project name is missing or invalid")
    return name.strip()


def _build_archive(project_root: Path, archive_path: Path) -> None:
    with zipfile.ZipFile(archive_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for folder_name in ("mcps", "skills", "tools"):
            _write_directory(archive, project_root, project_root / folder_name)

        for file_name in ("agent.yaml", "prompt.md"):
            source = project_root / file_name
            archive.write(source, arcname=file_name)


def _write_directory(archive: zipfile.ZipFile, project_root: Path, directory: Path) -> None:
    relative_dir = directory.relative_to(project_root).as_posix()
    archive.writestr(f"{relative_dir}/", "")

    for child in sorted(directory.iterdir(), key=lambda path: path.name):
        if child.is_dir():
            _write_directory(archive, project_root, child)
        else:
            archive.write(child, arcname=child.relative_to(project_root).as_posix())
