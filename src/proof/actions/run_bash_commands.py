from proof.actions import AnalysisContext, SessionContext
import subprocess

class RunBashCommands():
    def __init__(self, analysis_context: AnalysisContext, session_context: SessionContext):
        self.analysis_context = analysis_context
        self.session_context = session_context

    def create(self) -> None:
        pass

    def start(self) -> None:
        root = self.analysis_context.analysis_root
        pkg_manager = self.analysis_context.pkg_manager
        notebook_name = self.session_context.notebook_name
        subprocess.run(
            [pkg_manager, "run", "marimo", "edit", "--watch", notebook_name],
            cwd=root,
            check=True
        )