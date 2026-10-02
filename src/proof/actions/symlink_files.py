from proof.config import (
    PROOF_FILE_PATH,
    PROOF_PROJECT_CONTEXT_FILE_NAME,
    ANALYSIS_CONTEXT_FILE_PATH,
    CLAUDE_AGENT_FILES_PATH

)
from proof.actions import ProjectContext, AnalysisContext
from proof.utils import symlink

import os


class SymlinkFiles:
    def __init__(self, project_context: ProjectContext, analysis_context: AnalysisContext):
        self.project_context = project_context
        self.analysis_context = analysis_context

    def create(self) -> None:
        project_root = self.project_context.project_root
        analysis_root = self.analysis_context.analysis_root

        symlink(
            source=(project_root / PROOF_FILE_PATH / PROOF_PROJECT_CONTEXT_FILE_NAME),
            destination=(analysis_root / PROOF_PROJECT_CONTEXT_FILE_NAME)
        )

    def add(self, path: str) -> None:
        project_root = self.project_context.project_root
        analysis_root = self.analysis_context.analysis_root
        analysis_name = self.analysis_context.analysis_name
        source = project_root / path

        symlink(
            source=source,
            destination=(analysis_root / ANALYSIS_CONTEXT_FILE_PATH / source.name),
        )


