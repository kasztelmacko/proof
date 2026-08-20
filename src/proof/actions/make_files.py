from proof.actions.context import AnalysisContext
from proof.config import ( 
    PROOF_FILE_PATH,
    PROOF_PROJECT_CONTEXT_FILE_NAME,
    DEFAULT_MARIMO_NOTEBOOK_FILE_NAME, 
    ANALYSIS_CONTEXT_FILE_PATH,
    ANALYSIS_PLAN_FILE_NAME,
    ANALYSIS_OVERVIEW_FILE_NAME,
    MARIMO_NOTEBOOK_FILE_EXTENSION,
)


class MakeFiles():
    def __init__(self, analysis_context: AnalysisContext):
        self.analysis_context = analysis_context

    def create(self, notebook_name: str = DEFAULT_MARIMO_NOTEBOOK_FILE_NAME) -> None:
        project_root = self.analysis_context.project_root
        analysis_root = self.analysis_context.analysis_root
        notebook_file = notebook_name + MARIMO_NOTEBOOK_FILE_EXTENSION

        (project_root / PROOF_FILE_PATH / PROOF_PROJECT_CONTEXT_FILE_NAME).touch()
        (analysis_root / notebook_file).touch()
        (analysis_root / ANALYSIS_CONTEXT_FILE_PATH / ANALYSIS_PLAN_FILE_NAME).touch()
        (analysis_root / ANALYSIS_CONTEXT_FILE_PATH / ANALYSIS_OVERVIEW_FILE_NAME).touch()

    def add(self, notebook_name: str) -> None:
        analysis_root = self.analysis_context.analysis_root
        notebook_file = notebook_name + MARIMO_NOTEBOOK_FILE_EXTENSION
        (analysis_root / notebook_file).touch()