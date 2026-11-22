from proof.actions.context import AnalysisContext, ProjectContext
from proof.agent_tools import render_proof_toml
from proof.config import (
    PROOF_CONFIG_FILE_NAME,
    PROOF_DOTENV_FILE_NAME,
    PROOF_DOTENV_TEMPLATE,
    PROOF_FILE_PATH,
)


class WriteToFiles:
    def __init__(
        self,
        project_context: ProjectContext,
        analysis_context: AnalysisContext | None = None,
    ):
        self.project_context = project_context
        self.analysis_context = analysis_context

    def init(self, agent_tool: str) -> None:
        proof_dir = self.project_context.project_root / PROOF_FILE_PATH
        config_path = proof_dir / PROOF_CONFIG_FILE_NAME
        config_path.write_text(
            render_proof_toml(self.project_context.pkg_manager, agent_tool),
            encoding="utf-8",
        )
        env_path = proof_dir / PROOF_DOTENV_FILE_NAME
        if not env_path.exists():
            env_path.write_text(PROOF_DOTENV_TEMPLATE, encoding="utf-8")
