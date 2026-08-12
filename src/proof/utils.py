from collections.abc import Callable
from pathlib import Path
import sys
import os
import typer

from proof.errors import CLI_ERRORS
from proof.config import (
    PkgManager,
    PACKAGE_MANAGER_INDICATORS
)


def run_command(action: Callable[[], None]) -> None:
    try:
        action()
    except CLI_ERRORS as exc:
        print(exc, file=sys.stderr)
        raise typer.Exit(1) from None

def get_project_and_analysis_root(analysis_name: str) -> tuple[Path, Path]:
    project_root = Path.cwd()
    analysis_root = project_root / analysis_name
    return project_root, analysis_root

def detect_pkg_manager(project_root: Path) -> PkgManager:
    for indicator_tuple, pkg_manager in PACKAGE_MANAGER_INDICATORS.items():
        if any((project_root / indicator).exists() for indicator in indicator_tuple):
            return pkg_manager


def symlink(source: Path, destination: Path):
    source = source.resolve()

    os.symlink(source, destination, target_is_directory=source.is_dir())
