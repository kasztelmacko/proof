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

        if pkg_manager == "poetry":
            subprocess.run(
                ["poetry", "add", *REQUIRED_DEPENDENCIES],
                cwd=project_root,
                check=True,
            )
        elif pkg_manager == "uv":
            subprocess.run(
                ["uv", "pip", "install", *REQUIRED_DEPENDENCIES],
                cwd=project_root,
                check=True,
            )
        elif pkg_manager == "pip":
            subprocess.run(
                ["pip", "install", *REQUIRED_DEPENDENCIES],
                cwd=project_root,
                check=True,
            )
        elif pkg_manager == "conda":
            subprocess.run(
                ["conda", "install", *REQUIRED_DEPENDENCIES],
                cwd=project_root,
                check=True,
            )
        else:
            raise ValueError(f"Invalid package manager: {pkg_manager}")