from proof.config import (
    PROOF_TEMPLATE_ENV_FILE_NAME
)
from proof.actions import AnalysisContext

from importlib.resources import as_file, files
from shutil import copyfile


class CopyFiles:
    def __init__(self, analysis_context: AnalysisContext):
        self.analysis_context = analysis_context

    def create(self) -> None:
        root = self.analysis_context.analysis_root

        template_auth = files("proof.templates").joinpath(PROOF_TEMPLATE_ENV_FILE_NAME)

        with as_file(template_auth) as src:
            copyfile(src, root / ".env")