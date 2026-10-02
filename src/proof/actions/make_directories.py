from proof.actions.context import ProjectContext, AnalysisContext
from proof.config import (
    ANALYSIS_CONTEXT_FILE_PATH,
    ANALYSIS_NOTES_FILE_PATH,
    ANALYSIS_NOTES_IMAGES_FILE_PATH,
    PROOF_FILE_PATH
)

class MakeDirectories():
    def __init__(
        self, 
        project_context: ProjectContext, 
        analysis_context: AnalysisContext | None = None
    ):
        self.project_context = project_context
        self.analysis_context = analysis_context

    def init(self) -> None:
        project_root = self.project_context.project_root
        proof_dir = (project_root / PROOF_FILE_PATH)

        if not proof_dir.exists():
            proof_dir.mkdir(parents=True)

    def create(self) -> None:
        analysis_root = self.analysis_context.analysis_root

        analysis_root.mkdir(parents=True)
        (analysis_root / ANALYSIS_NOTES_FILE_PATH).mkdir(parents=True)
        (analysis_root / ANALYSIS_NOTES_IMAGES_FILE_PATH).mkdir(parents=True)
        (analysis_root / ANALYSIS_CONTEXT_FILE_PATH).mkdir(parents=True)