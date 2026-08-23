from proof.actions.context import AnalysisContext
from proof.utils import (
    print_app_title, 
    print_commands_table, 
    print_skills_table
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


