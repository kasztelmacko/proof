from proof.actions.context import AnalysisContext


class MakeDirectories():
    def __init__(self, analysis_context: AnalysisContext):
        self.analysis_context = analysis_context

    def create(self) -> None:
        root = self.analysis_context.analysis_root
        root.mkdir()
        (root / "notes").mkdir()
        (root / "context").mkdir()