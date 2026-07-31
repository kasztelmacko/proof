from proof.actions.context import AnalysisContext
from proof.config import (
    CONTEXT_FILE_PATH,
    NOTES_FILE_PATH
)

class MakeDirectories():
    def __init__(self, analysis_context: AnalysisContext):
        self.analysis_context = analysis_context

    def create(self) -> None:
        root = self.analysis_context.analysis_root
        root.mkdir()
        (root / NOTES_FILE_PATH).mkdir(parents=True)
        (root / CONTEXT_FILE_PATH).mkdir(parents=True)