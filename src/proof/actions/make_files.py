from proof.actions.context import AnalysisContext


class MakeFiles():
    def __init__(self, context: AnalysisContext):
        self.context = context

    def create(self) -> None:
        root = self.context.analysis_root
        (root / "notebook.py").touch()