from proof.actions.context import AnalysisContext
from proof.config import REQUIRED_DEPENDENCIES
import subprocess

class InstallDependencies():
    def __init__(self, analysis_context: AnalysisContext):
        self.analysis_context = analysis_context

    def create(self) -> None:
        pkg_manager = self.analysis_context.pkg_manager
        root = self.analysis_context.analysis_root

        if pkg_manager == "poetry":
            subprocess.run(
                ["poetry", "add", *REQUIRED_DEPENDENCIES],
                cwd=root,
                check=True,
            )
        elif pkg_manager == "uv":
            subprocess.run(
                ["uv", "pip", "install", *REQUIRED_DEPENDENCIES],
                cwd=root,
                check=True,
            )
        elif pkg_manager == "pip":
            subprocess.run(
                ["pip", "install", *REQUIRED_DEPENDENCIES],
                cwd=root,
                check=True,
            )
        elif pkg_manager == "conda":
            subprocess.run(
                ["conda", "install", *REQUIRED_DEPENDENCIES],
                cwd=root,
                check=True,
            )
        else:
            raise ValueError(f"Invalid package manager: {pkg_manager}")