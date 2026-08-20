from proof.config import (
    PROOF_COPY_FILES_PATH,
    PROOF_ENV_FILE_NAME,
    PROOF_FILE_PATH,
    ANALYSIS_SKILLS_FILES_PATH,
    CLAUDE_AGENT_FILES_PATH,
    CLAUDE_SETTINGS_FILE_NAME
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
        agent_settings_file = copy_files_root.joinpath(CLAUDE_SETTINGS_FILE_NAME)
        skills_copy_files = copy_files_root.joinpath(ANALYSIS_SKILLS_FILES_PATH)

        with as_file(env_copy_file) as src:
            shutil.copyfile(src, analysis_root / ".env")

        with as_file(agent_settings_file) as settings:
            shutil.copyfile(settings, analysis_root / CLAUDE_AGENT_FILES_PATH / CLAUDE_SETTINGS_FILE_NAME)

        with as_file(skills_copy_files) as src:
            shutil.copytree(src, analysis_root / CLAUDE_AGENT_FILES_PATH / ANALYSIS_SKILLS_FILES_PATH, dirs_exist_ok=True)


