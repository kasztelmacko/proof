from proof.actions.context import AnalysisContext
from proof.config import PROOF_CONFIG_FILE_NAME


class WriteConfig():
    def __init__(self, context: AnalysisContext):
        self.context = context

    def create(self) -> None:
        config_path = self.context.analysis_root / PROOF_CONFIG_FILE_NAME
        config_path.write_text(
            f'pkg_manager = "{self.context.pkg_manager}"\n',
            encoding="utf-8"
        )
