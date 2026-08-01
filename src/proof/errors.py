class ProofError(Exception):
    pass

class ToolNotFoundException(ProofError):
    def __init__(self, tool_name: str, install_hint: str | None = None):
        message = f"Required tool not found on PATH: {tool_name}"
        if install_hint:
            message = f"{message}\n{install_hint}"
        super().__init__(message)


CLI_ERRORS = (ProofError, )