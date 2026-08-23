from proof.config import (
    PROOF_COPY_FILES_PATH,
    PROOF_ENV_FILE_NAME,
    CLAUDE_AGENT_FILES_PATH,
)
from proof.actions import AnalysisContext

from importlib.resources import as_file, files
import shutil


class CopyFiles:
    def __init__(self, analysis_context: AnalysisContext):
        self.analysis_context = analysis_context

    def create(self) -> None:
        analysis_root = self.analysis_context.analysis_root
        copy_files_root = files("proof").joinpath(PROOF_COPY_FILES_PATH)

        env_copy_file = copy_files_root.joinpath(PROOF_ENV_FILE_NAME)
        claude_agent_copy_files = copy_files_root.joinpath(CLAUDE_AGENT_FILES_PATH)

        with as_file(env_copy_file) as src:
            shutil.copyfile(src, analysis_root / ".env")

        with as_file(claude_agent_copy_files) as src:
            shutil.copytree(src, analysis_root / CLAUDE_AGENT_FILES_PATH, dirs_exist_ok=True)


