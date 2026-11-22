import shutil

from proof.actions.context import AnalysisContext, ProjectContext, SessionContext
from proof.actions.sessions.agent_models import (
    load_agent_models,
    load_agent_tool_name,
)
from proof.actions.sessions.manage_session import read_sessions
from proof.actions.sessions.start_session import (
    build_session_env,
    run_agent_process,
    start_notebook_session,
)
from proof.agent_tools import command_session_id, get_tool
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
        self.notebook_process = None

    def init(self, agent_tool: str) -> None:
        self._require_tool(
            "curl",
            "Install curl: https://curl.se/download.html",
        )
        self._require_tool(
            "jq",
            "Install jq: https://jqlang.org/download/",
        )
        self._require_tool(
            "uvx",
            "Install uv: https://docs.astral.sh/uv/getting-started/installation/",
        )
        tool = get_tool(agent_tool)
        self._require_tool(tool.binary, tool.install_hint)

    def start(self) -> None:
        self._launch(resume=False)

    def resume(self) -> None:
        self._launch(resume=True)

    def _launch(self, *, resume: bool) -> None:
        project_root = self.project_context.project_root
        analysis_root = self.analysis_context.analysis_root
        tool = get_tool(load_agent_tool_name(project_root))
        harness = load_agent_models(project_root)["harness"]
        env = build_session_env(project_root, analysis_root)
        session_name = self.session_context.session_name
        stored = read_sessions(analysis_root).get(session_name)
        self.notebook_process = start_notebook_session(
            analysis_root=analysis_root,
            pkg_manager=self.project_context.pkg_manager,
            notebook_name=self.session_context.notebook_name,
            notebook_port=self.session_context.notebook_port,
            env=env,
        )
        run_agent_process(
            analysis_root=analysis_root,
            notebook_port=self.session_context.notebook_port,
            env=env,
            tool=tool,
            session_id=command_session_id(tool, session_name, stored),
            model_id=harness.model_id,
            effort=harness.effort,
            resume=resume,
            has_stored_id=stored is not None,
        )

    def _require_tool(self, tool_name: str, install_hint: str) -> None:
        if shutil.which(tool_name) is None:
            raise ToolNotFoundException(
                tool_name=tool_name,
                install_hint=install_hint,
            )
