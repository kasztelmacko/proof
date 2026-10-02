from proof.actions.context import ProjectContext, AnalysisContext
from proof.config import (
    PROOF_CONFIG_FILE_NAME, 
    PROOF_FILE_PATH
)
from shutil import copyfile


class WriteToFiles():
    def __init__(
        self, 
        project_context: ProjectContext, 
        analysis_context: AnalysisContext | None = None
    ):
        self.project_context = project_context
        self.analysis_context = analysis_context

    def init(self) -> None:
        config_path = self.project_context.project_root / PROOF_FILE_PATH / PROOF_CONFIG_FILE_NAME
        config_path.write_text(
            f'pkg_manager = "{self.project_context.pkg_manager}"\n',
            encoding="utf-8"
        )

