from proof.actions.context import AnalysisContext, ProjectContext
from proof.actions.sessions.agent_models import apply_agent_models, load_agent_models


class ApplyAgentModels:
    def __init__(
        self,
        project_context: ProjectContext,
        analysis_context: AnalysisContext | None = None,
    ):
        self.project_context = project_context
        self.analysis_context = analysis_context

    def start(self) -> None:
        models = load_agent_models(self.project_context.project_root)
        apply_agent_models(self.analysis_context.analysis_root, models)

    def resume(self) -> None:
        self.start()
