from proof.actions import AnalysisContext, SessionContext
from proof.config import MARIMO_NOTEBOOK_EDIT_BASH
import subprocess
import shutil

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
        subprocess.Popen(
            [pkg_manager, *MARIMO_NOTEBOOK_EDIT_BASH, notebook_name],
            cwd=root,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            [shutil.which("pi")],
            cwd=root,
            check=True
        )
