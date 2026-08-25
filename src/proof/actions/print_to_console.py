from proof.actions.context import AnalysisContext
from proof.actions.styling.console_prints import (
    print_app_title, 
    print_commands_table, 
    print_skills_table,
    print_user_tip,
)

from rich.console import Console


class PrintToConsole():
    def __init__(self, analysis_context: AnalysisContext):
        self.analysis_context = analysis_context

    def create(self) -> None:
        console = Console()
        print_app_title(console=console)
        print_commands_table(console=console)
        print_skills_table(console=console)
        print_user_tip(console=console)


