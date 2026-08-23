from proof.actions.context import AnalysisContext
from proof.config import (
    ANALYSIS_CONTEXT_FILE_PATH,
    ANALYSIS_NOTES_FILE_PATH,
    CLAUDE_AGENT_FILES_PATH,
    ANALYSIS_SKILLS_FILES_PATH,
    PROOF_FILE_PATH
)

class MakeDirectories():
    def __init__(self, analysis_context: AnalysisContext):
        self.analysis_context = analysis_context

    def create(self) -> None:
        analysis_root = self.analysis_context.analysis_root
        project_root = self.analysis_context.project_root
        analysis_name = self.analysis_context.analysis_name

        proof_config_dir = (project_root / PROOF_FILE_PATH)
        
        if not proof_config_dir.exists():
            proof_config_dir.mkdir(parents=True)

        (project_root / analysis_name).mkdir(parents=True)

        (analysis_root / ANALYSIS_NOTES_FILE_PATH).mkdir(parents=True)
        (analysis_root / ANALYSIS_CONTEXT_FILE_PATH).mkdir(parents=True)