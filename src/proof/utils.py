from collections.abc import Callable
from pathlib import Path
import os
import shutil
import typer
from rich.console import Console


from proof.exceptions import (
    CLI_ERRORS,
    AnalysisNotFoundException,
    NotebookNotFoundException,
    ProofNotInitializedException,
)
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


def require_proof_initialized(project_root: Path) -> None:
    proof_dir = project_root / PROOF_FILE_PATH
    context_file = proof_dir / PROOF_PROJECT_CONTEXT_FILE_NAME
    if not proof_dir.is_dir() or not context_file.is_file():
        raise ProofNotInitializedException()

def get_analysis_root(project_root: Path, analysis_name: str) -> Path:
    return project_root / PROOF_FILE_PATH / analysis_name


def require_analysis_exists(project_root: Path, analysis_name: str) -> None:
    analysis_root = get_analysis_root(project_root, analysis_name)
    if not analysis_root.is_dir():
        raise AnalysisNotFoundException(analysis_name)


def require_notebook_exists(analysis_root: Path, analysis_name: str, notebook_name: str) -> None:
    if not (analysis_root / notebook_name).is_file():
        raise NotebookNotFoundException(notebook_name, analysis_name)


def detect_pkg_manager(project_root: Path) -> PkgManager:
    for indicator_tuple, pkg_manager in PACKAGE_MANAGER_INDICATORS.items():
        if any((project_root / indicator).exists() for indicator in indicator_tuple):
            return pkg_manager


def symlink(source: Path, destination: Path):
    source = source.resolve()

    try:
        os.symlink(source, destination, target_is_directory=source.is_dir())
    except OSError:
        if source.is_dir():
            shutil.copytree(source, destination)
            return
        try:
            os.link(source, destination)
        except OSError:
            shutil.copy2(source, destination)


def project_context_is_empty(project_root: Path) -> bool:
    context_path = (
        project_root
        / PROOF_FILE_PATH
        / PROOF_PROJECT_CONTEXT_FILE_NAME
    )
    if not context_path.exists():
        return True
    return context_path.read_text(encoding="utf-8").strip() == ""

