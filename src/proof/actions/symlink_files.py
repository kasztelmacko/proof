from proof.actions import AnalysisContext, ProjectContext
from proof.config import (
    ANALYSIS_CONTEXT_FILE_PATH,
    PROOF_FILE_PATH,
    PROOF_PROJECT_CONTEXT_FILE_NAME,
)
from proof.utils import symlink


class SymlinkFiles:
    def __init__(
        self, project_context: ProjectContext, analysis_context: AnalysisContext
    ):
        self.project_context = project_context
        self.analysis_context = analysis_context

    def create(self) -> None:
        project_root = self.project_context.project_root
        analysis_root = self.analysis_context.analysis_root

        symlink(
            source=(project_root / PROOF_FILE_PATH / PROOF_PROJECT_CONTEXT_FILE_NAME),
            destination=(analysis_root / PROOF_PROJECT_CONTEXT_FILE_NAME),
        )

    def add(self, path: str) -> None:
        project_root = self.project_context.project_root
        analysis_root = self.analysis_context.analysis_root
        source = project_root / path

        symlink(
            source=source,
            destination=(analysis_root / ANALYSIS_CONTEXT_FILE_PATH / source.name),
        )
