from proof.actions.context import AnalysisContext, ProjectContext
from proof.actions.sessions.agent_models import (
    load_agent_models,
    load_agent_tool_name,
)
from proof.actions.sessions.project_files import project_agent_files
from proof.agent_tools import get_tool


class ApplyAgentModels:
    def __init__(
        self,
        project_context: ProjectContext,
        analysis_context: AnalysisContext | None = None,
    ):
        self.project_context = project_context
        self.analysis_context = analysis_context

    def start(self) -> None:
        project_root = self.project_context.project_root
        tool = get_tool(load_agent_tool_name(project_root))
        models = load_agent_models(project_root)
        project_agent_files(self.analysis_context.analysis_root, tool, models)

    def resume(self) -> None:
        self.start()
