from proof.actions.context import ProjectContext, AnalysisContext
from proof.actions.styling.console_prints import (
    print_app_title, 
    print_commands_table, 
    print_skills_table,
    print_create_success,
    print_user_tip,
)
from proof.config import PROOF_FILE_PATH, PROOF_PROJECT_CONTEXT_FILE_NAME
from proof.utils import project_context_is_empty

from rich.console import Console


class PrintToConsole():
    def __init__(
        self, 
        project_context: ProjectContext,
        analysis_context: AnalysisContext | None = None
    ):
        self.project_context = project_context
        self.analysis_context = analysis_context

    def init(self) -> None:
        console = Console()
        print_app_title(console=console)
        print_commands_table(console=console)
        print_skills_table(console=console)
        print_user_tip(console=console)

    def create(self) -> None:
        project_root = self.project_context.project_root 
        console = Console()
        print_create_success(
            console=console,
            analysis_name=self.analysis_context.analysis_name,
        )
        if project_context_is_empty(project_root=project_root):
            print_user_tip(console=console)


