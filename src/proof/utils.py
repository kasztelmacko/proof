from collections.abc import Callable
from pathlib import Path
import sys
import os
import typer
from rich.console import Console
from rich.table import Table
from rich_pyfiglet import RichFiglet

from proof.errors import CLI_ERRORS
from proof.config import (
    PkgManager,
    PACKAGE_MANAGER_INDICATORS,
    PROOF_HELPER_FIRST_COL_WIDTH
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

def print_app_title(console: Console) -> None:
    app_title = RichFiglet(
        text="proof",
        font="ansi_shadow",
        colors=["white"],
    )
    console.print(app_title)

def print_commands_table(console: Console) -> None:
    table = Table(box=None, show_header=True, pad_edge=False)
    console.print("")
    table.add_column("Command", style="dim", min_width=PROOF_HELPER_FIRST_COL_WIDTH, no_wrap=True)
    table.add_column("Description")
    table.add_row("proof create [cyan]<analysis_name>[/cyan]", "Create a new analysis")
    table.add_row("proof start [cyan]<analysis_name> <notebook_name>[/cyan]", "Start a marimo notebook session")
    table.add_row("proof add notebook [cyan]<analysis_name> <notebook_name>[/cyan]", "Add a notebook to an analysis")
    table.add_row("proof add symlink [cyan]<analysis_name> <path>[/cyan]", "Symlink a project file into an analysis")
    console.print(table)

def print_skills_table(console: Console) -> None:
    table = Table(box=None, show_header=True, pad_edge=False)
    console.print("")
    table.add_column("Skill", style="dim", min_width=PROOF_HELPER_FIRST_COL_WIDTH, no_wrap=True)
    table.add_column("Description")
    table.add_row("/proof-plan", "Plan analysis based on user provided context")
    table.add_row("/proof-summarize-step", "Write the summary of currently analyzed step to `analysis_overview.md`")
    table.add_row("/proof-help-analyze", "Analyze step or deepen user understanding")
    console.print(table)


