class ProofError(Exception):
    pass


class ProofNotInitializedException(ProofError):
    def __init__(self):
        super().__init__("Proof is not initialized. Run [cyan]proof init[/cyan] first.")


class AnalysisNotFoundException(ProofError):
    def __init__(self, analysis_name: str):
        super().__init__(
            f"Analysis [cyan]{analysis_name}[/cyan] was not found"
        )


class NotebookNotFoundException(ProofError):
    def __init__(self, notebook_name: str, analysis_name: str):
        super().__init__(
            f"Notebook [cyan]{notebook_name}[/cyan] was not found in analysis [cyan]{analysis_name}[/cyan]. Remember, that the notebook name is the name of the file in the analysis directory with the .py extension."
        )


class SessionNotFoundException(ProofError):
    def __init__(self, session_name: str, analysis_name: str):
        super().__init__(
            f"Agent session [cyan]{session_name}[/cyan] was not found in analysis [cyan]{analysis_name}[/cyan]"
        )


class AgentConfigException(ProofError):
    def __init__(self, message: str):
        super().__init__(message)


class ToolNotFoundException(ProofError):
    def __init__(self, tool_name: str, install_hint: str | None = None):
        message = f"Required tool not found on PATH: [cyan]{tool_name}[/cyan]"
        if install_hint:
            message = f"{message}\n{install_hint}"
        super().__init__(message)

CLI_ERRORS = (ProofNotInitializedException, AnalysisNotFoundException, NotebookNotFoundException, SessionNotFoundException, AgentConfigException, ToolNotFoundException)
