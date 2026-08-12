class ProofError(Exception):
    pass

class ToolNotFoundException(ProofError):
    def __init__(self, tool_name: str, install_hint: str | None = None):
        message = f"Required tool not found on PATH: {tool_name}"
        if install_hint:
            message = f"{message}\n{install_hint}"
        super().__init__(message)    

class MarimoNotebookStartupTimeout(ProofError):
    def __init__(self, notebook_name: str, notebook_port: str):
        message = f"marimo notebook {notebook_name} did not start succesfully on port {notebook_port}"
        super().__init__(message)

CLI_ERRORS = (ProofError, )