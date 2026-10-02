from proof.actions.context import ProjectContext, AnalysisContext
from proof.config import ( 
    PROOF_FILE_PATH,
    PROOF_PROJECT_CONTEXT_FILE_NAME,
    DEFAULT_MARIMO_NOTEBOOK_FILE_NAME, 
    ANALYSIS_CONTEXT_FILE_PATH,
    ANALYSIS_PLAN_FILE_NAME,
    ANALYSIS_OVERVIEW_FILE_NAME,
    ANALYSIS_NOTES_FILE_PATH,
    MARIMO_NOTEBOOK_FILE_EXTENSION,
    ANALYSIS_NOTEST_FILE_NAME
)


class MakeFiles():
    def __init__(
        self, 
        project_context: ProjectContext, 
        analysis_context: AnalysisContext | None = None
    ):
        self.project_context = project_context
        self.analysis_context = analysis_context

    def init(self) -> None:
        project_root = self.project_context.project_root

        (project_root / PROOF_FILE_PATH / PROOF_PROJECT_CONTEXT_FILE_NAME).touch()

    def create(self, notebook_name: str = DEFAULT_MARIMO_NOTEBOOK_FILE_NAME) -> None:
        analysis_root = self.analysis_context.analysis_root
        notebook_file = notebook_name + MARIMO_NOTEBOOK_FILE_EXTENSION

        (analysis_root / notebook_file).touch()
        (analysis_root / ANALYSIS_CONTEXT_FILE_PATH / ANALYSIS_PLAN_FILE_NAME).touch()
        (analysis_root / ANALYSIS_CONTEXT_FILE_PATH / ANALYSIS_OVERVIEW_FILE_NAME).touch()
        (analysis_root / ANALYSIS_NOTES_FILE_PATH / ANALYSIS_NOTEST_FILE_NAME).touch()

    def add(self, notebook_name: str) -> None:
        analysis_root = self.analysis_context.analysis_root
        notebook_file = notebook_name + MARIMO_NOTEBOOK_FILE_EXTENSION

        (analysis_root / notebook_file).touch()