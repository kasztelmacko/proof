from proof.actions.context import AnalysisContext, ProjectContext, SessionContext
from proof.actions.sessions.manage_session import (
    read_session_names,
    require_session_exists,
    write_session_names,
)


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
        names = read_session_names(analysis_root)
        if session_name not in names:
            names.append(session_name)
            write_session_names(analysis_root, names)

    def resume(self) -> None:
        require_session_exists(
            analysis_root=self.analysis_context.analysis_root,
            analysis_name=self.analysis_context.analysis_name,
            session_name=self.session_context.session_name,
        )
