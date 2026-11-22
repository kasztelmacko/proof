from proof.actions.context import AnalysisContext, ProjectContext, SessionContext
from proof.actions.sessions.agent_models import load_agent_tool_name
from proof.actions.sessions.manage_session import (
    read_sessions,
    require_session_exists,
    write_sessions,
)
from proof.agent_tools import allocate_session_id, get_tool


class SaveAgentSession:
    def __init__(
        self,
        project_context: ProjectContext,
        analysis_context: AnalysisContext,
        session_context: SessionContext,
    ):
        self.project_context = project_context
        self.analysis_context = analysis_context
        self.session_context = session_context

    def start(self) -> None:
        analysis_root = self.analysis_context.analysis_root
        session_name = self.session_context.session_name
        tool = get_tool(load_agent_tool_name(self.project_context.project_root))
        sessions = read_sessions(analysis_root)
        if session_name not in sessions:
            sessions[session_name] = allocate_session_id(tool, session_name)
            write_sessions(analysis_root, sessions)

    def resume(self) -> None:
        require_session_exists(
            analysis_root=self.analysis_context.analysis_root,
            analysis_name=self.analysis_context.analysis_name,
            session_name=self.session_context.session_name,
        )
