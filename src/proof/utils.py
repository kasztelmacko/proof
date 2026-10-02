from collections.abc import Callable
from pathlib import Path
import sys
import os
import typer


from proof.errors import CLI_ERRORS
from proof.config import (
    PkgManager,
    PACKAGE_MANAGER_INDICATORS,
    PROOF_FILE_PATH,
    PROOF_HELPER_FIRST_COL_WIDTH
)


def run_command(action: Callable[[], None]) -> None:
    try:
        action()
    except CLI_ERRORS as exc:
        print(exc, file=sys.stderr)
        raise typer.Exit(1) from None

def get_project_root() -> Path:
    return Path.cwd()

def get_analysis_root(project_root: Path, analysis_name: str) -> Path:
    return project_root / PROOF_FILE_PATH / analysis_name


def get_project_and_analysis_root(
    analysis_name: str | None = None,
) -> tuple[Path, Path | None]:
    project_root = get_project_root()
    analysis_root = (
        get_analysis_root(project_root, analysis_name)
        if analysis_name is not None
        else None
    )
    return project_root, analysis_root

def detect_pkg_manager(project_root: Path) -> PkgManager:
    for indicator_tuple, pkg_manager in PACKAGE_MANAGER_INDICATORS.items():
        if any((project_root / indicator).exists() for indicator in indicator_tuple):
            return pkg_manager


def symlink(source: Path, destination: Path):
    source = source.resolve()

    os.symlink(source, destination, target_is_directory=source.is_dir())




