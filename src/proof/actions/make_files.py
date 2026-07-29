from proof.actions.context import AnalysisContext
from proof.config import PROOF_CONFIG_FILE_NAME, NOTEBOOK_FILE_NAME


class MakeFiles():
    def __init__(self, context: AnalysisContext):
        self.context = context

    def create(self) -> None:
        root = self.context.analysis_root
        (root / NOTEBOOK_FILE_NAME).touch()
        (root / PROOF_CONFIG_FILE_NAME).touch()