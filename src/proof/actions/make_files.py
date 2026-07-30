from proof.actions.context import AnalysisContext
from proof.config import PROOF_CONFIG_FILE_NAME, DEFAULT_NOTEBOOK_FILE_NAME


class MakeFiles():
    def __init__(self, analysis_context: AnalysisContext):
        self.analysis_context = analysis_context

    def create(self, notebook_name: str = DEFAULT_NOTEBOOK_FILE_NAME) -> None:
        root = self.analysis_context.analysis_root
        notebook_file = notebook_name + ".py"
        (root / notebook_file).touch()
        (root / PROOF_CONFIG_FILE_NAME).touch()