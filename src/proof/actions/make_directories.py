from proof.actions.context import AnalysisContext


class MakeDirectories():
    def __init__(self, context: AnalysisContext):
        self.context = context

    def create(self) -> None:
        root = self.context.analysis_root
        root.mkdir()
        (root / "notes").mkdir()
        (root / "context").mkdir()