from proof.actions.context import AnalysisContext
from proof.config import ( 
    DEFAULT_MARIMO_NOTEBOOK_FILE_NAME, 
    PROOF_FILE_PATH,
    PROOF_PROJECT_CONTEXT_FILE_NAME
)


class MakeFiles():
    def __init__(self, analysis_context: AnalysisContext):
        self.analysis_context = analysis_context

    def create(self, notebook_name: str = DEFAULT_MARIMO_NOTEBOOK_FILE_NAME) -> None:
        project_root = self.analysis_context.project_root
        analysis_root = self.analysis_context.analysis_root
        notebook_file = notebook_name + ".py"

        (project_root / PROOF_FILE_PATH / PROOF_PROJECT_CONTEXT_FILE_NAME).touch()
        (analysis_root / notebook_file).touch()