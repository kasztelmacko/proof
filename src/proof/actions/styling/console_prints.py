from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich_pyfiglet import RichFiglet

from proof.config import (
    PROOF_HELPER_FIRST_COL_WIDTH
)

def print_app_title(console: Console) -> None:
    app_title = RichFiglet(
        text=r"proof",
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

def print_user_tip(console: Console) -> None:
    console.print("")
    console.print(
        Panel(
            "Remember to fill project context in [cyan].proof/CLAUDE.md[/cyan].  "
            "It is the primary source of truth about the project scope and its innerworkings",
        )
    )
