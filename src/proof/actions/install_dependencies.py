from proof.actions.context import ProjectContext, AnalysisContext
from proof.config import REQUIRED_DEPENDENCIES
import subprocess

class InstallDependencies():
    def __init__(
            self, 
            project_context: ProjectContext, 
            analysis_context: AnalysisContext | None = None
        ):
        self.project_context = project_context
        self.analysis_context = analysis_context

    def init(self) -> None:
        pkg_manager = self.project_context.pkg_manager
        project_root = self.project_context.project_root

        INSTALL_COMMANDS = {
            "poetry": ["poetry", "add"],
            "uv": ["uv", "pip", "install"],
            "pip": ["pip", "install"],
            "conda": ["conda", "install", "-y"],
        }

        subprocess.run(
            [*INSTALL_COMMANDS[pkg_manager], *REQUIRED_DEPENDENCIES],
            cwd=project_root,
            check=True,
        )