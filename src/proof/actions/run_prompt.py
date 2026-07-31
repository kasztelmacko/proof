from proof.actions import AnalysisContext, SessionContext

class RunPrompts():
    def __init__(self, analysis_context: AnalysisContext, session_context: SessionContext):
        self.analysis_context = analysis_context
        self.session_context = session_context

    def start()