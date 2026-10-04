from collections.abc import Callable
from pathlib import Path
import os
import typer
from rich.console import Console


from proof.errors import CLI_ERRORS
from proof.config import (
    PkgManager,
    PACKAGE_MANAGER_INDICATORS,
    PROOF_FILE_PATH,
    PROOF_PROJECT_CONTEXT_FILE_NAME
)


def run_command(action: Callable[[], None]) -> None:
    try:
        action()
    except CLI_ERRORS as exc:
        Console(stderr=True).print(str(exc))
        raise typer.Exit(1) from None

def get_project_root() -> Path:
    return Path.cwd()

def get_analysis_root(project_root: Path, analysis_name: str) -> Path:
    return project_root / PROOF_FILE_PATH / analysis_name


def detect_pkg_manager(project_root: Path) -> PkgManager:
    for indicator_tuple, pkg_manager in PACKAGE_MANAGER_INDICATORS.items():
        if any((project_root / indicator).exists() for indicator in indicator_tuple):
            return pkg_manager


def symlink(source: Path, destination: Path):
    source = source.resolve()

    os.symlink(source, destination, target_is_directory=source.is_dir())


def project_context_is_empty(project_root: Path) -> bool:
    context_path = (
        project_root
        / PROOF_FILE_PATH
        / PROOF_PROJECT_CONTEXT_FILE_NAME
    )
    if not context_path.exists():
        return True
    return context_path.read_text(encoding="utf-8").strip() == ""

