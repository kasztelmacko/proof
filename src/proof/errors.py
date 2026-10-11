class ProofError(Exception):
    pass

class SessionNotFoundException(ProofError):
    def __init__(self, session_name: str, sessions_file: str):
        super().__init__(
            f"Agent session [cyan]{session_name}[/cyan] was not found in [cyan]{sessions_file}[/cyan]"
        )


class ToolNotFoundException(ProofError):
    def __init__(self, tool_name: str, install_hint: str | None = None):
        message = f"Required tool not found on PATH: [cyan]{tool_name}[/cyan]"
        if install_hint:
            message = f"{message}\n{install_hint}"
        super().__init__(message)

CLI_ERRORS = (ProofError, )