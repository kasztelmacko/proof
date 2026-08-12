from proof.actions.context import AnalysisContext
from proof.config import (
    PROOF_CONFIG_FILE_NAME, 
    PROOF_FILE_PATH
)
from shutil import copyfile


class WriteToFiles():
    def __init__(self, analysis_context: AnalysisContext):
        self.analysis_context = analysis_context

    def create(self) -> None:
        config_path = self.analysis_context.project_root / PROOF_FILE_PATH / PROOF_CONFIG_FILE_NAME
        config_path.write_text(
            f'pkg_manager = "{self.analysis_context.pkg_manager}"\n',
            encoding="utf-8"
        )

