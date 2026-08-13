from proof.config import (
    PROOF_FILE_PATH,
    PROOF_PROJECT_CONTEXT_FILE_NAME,
    CLAUDE_AGENT_FILES_PATH

)
from proof.actions import AnalysisContext
from proof.utils import symlink

import os


class SymlinkFiles:
    def __init__(self, analysis_context: AnalysisContext):
        self.analysis_context = analysis_context

    def create(self) -> None:
        project_root = self.analysis_context.project_root
        analysis_root = self.analysis_context.analysis_root

        symlink(
            source=(project_root / PROOF_FILE_PATH / PROOF_PROJECT_CONTEXT_FILE_NAME),
            destination=(analysis_root / CLAUDE_AGENT_FILES_PATH / PROOF_PROJECT_CONTEXT_FILE_NAME)
        )



