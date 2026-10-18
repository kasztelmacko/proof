import os
import shutil

from dotenv import dotenv_values

from proof.actions import AnalysisContext, ProjectContext, SessionContext
from proof.actions.sessions.agent_models import load_agent_models
from proof.actions.sessions.start_session import (
    resume_agent_session,
    start_agent_session,
    start_notebook_session,
)
from proof.config import MARIMO_NOTEBOOK_TOKEN
from proof.exceptions import ToolNotFoundException


class RunBashCommands:
    def __init__(
        self,
        project_context: ProjectContext,
        analysis_context: AnalysisContext | None = None,
        session_context: SessionContext | None = None,
    ):
        self.project_context = project_context
        self.analysis_context = analysis_context
        self.session_context = session_context

    def init(self) -> None:
        if shutil.which("curl") is None:
            raise ToolNotFoundException(
                tool_name="curl",
                install_hint="Install curl: https://curl.se/download.html",
            )

        if shutil.which("jq") is None:
            raise ToolNotFoundException(
                tool_name="jq",
                install_hint="Install jq: https://jqlang.org/download/",
            )

        if shutil.which("uvx") is None:
            raise ToolNotFoundException(
                tool_name="uvx",
                install_hint="Install uv: https://docs.astral.sh/uv/getting-started/installation/",
            )

        if shutil.which("claude") is None:
            raise ToolNotFoundException(
                tool_name="claude",
                install_hint="Install Claude Code: https://code.claude.com/docs/en/",
            )

    def start(self) -> None:
        analysis_root = self.analysis_context.analysis_root
        pkg_manager = self.project_context.pkg_manager
        notebook_name = self.session_context.notebook_name
        notebook_port = self.session_context.notebook_port

        env = os.environ.copy()
        env.update(dotenv_values(analysis_root / ".env"))
        env["MARIMO_TOKEN"] = MARIMO_NOTEBOOK_TOKEN

        start_notebook_session(
            analysis_root=analysis_root,
            pkg_manager=pkg_manager,
            notebook_name=notebook_name,
            notebook_port=notebook_port,
            env=env,
        )
        harness = load_agent_models(self.project_context.project_root)["harness"]
        start_agent_session(
            analysis_root=analysis_root,
            notebook_port=notebook_port,
            env=env,
            session_name=self.session_context.session_name,
            model=harness.model_id,
            effort=harness.effort,
        )

    def resume(self) -> None:
        analysis_root = self.analysis_context.analysis_root
        pkg_manager = self.project_context.pkg_manager
        notebook_name = self.session_context.notebook_name
        notebook_port = self.session_context.notebook_port

        env = os.environ.copy()
        env.update(dotenv_values(analysis_root / ".env"))
        env["MARIMO_TOKEN"] = MARIMO_NOTEBOOK_TOKEN

        start_notebook_session(
            analysis_root=analysis_root,
            pkg_manager=pkg_manager,
            notebook_name=notebook_name,
            notebook_port=notebook_port,
            env=env,
        )
        harness = load_agent_models(self.project_context.project_root)["harness"]
        resume_agent_session(
            analysis_root=analysis_root,
            notebook_port=notebook_port,
            env=env,
            session_name=self.session_context.session_name,
            model=harness.model_id,
            effort=harness.effort,
        )
