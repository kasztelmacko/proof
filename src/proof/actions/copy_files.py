from proof.config import (
    PI_AGENT_PATH,
    PI_AGENT_AUTH_FILE_NAME
)
from proof.actions import AnalysisContext

from importlib.resources import as_file, files
from shutil import copyfile


class CopyFiles:
    def __init__(self, analysis_context: AnalysisContext):
        self.analysis_context = analysis_context

    def create(self) -> None:
        pi_auth_path = (
            self.analysis_context.analysis_root
            / PI_AGENT_PATH
            / PI_AGENT_AUTH_FILE_NAME
        )

        template_auth = files("proof.templates").joinpath(PI_AGENT_AUTH_FILE_NAME)

        with as_file(template_auth) as src:
            copyfile(src, pi_auth_path)