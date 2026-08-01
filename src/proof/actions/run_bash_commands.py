from proof.actions import AnalysisContext, SessionContext
from proof.config import (
    MARIMO_NOTEBOOK_EDIT_BASH,
    CLAUDE_STARTUP_MODEL,
    CLAUDE_STARTUP_EFFORT
)
from proof.errors import ToolNotFoundException
import subprocess
import shutil
import os
from dotenv import dotenv_values

class RunBashCommands():
    def __init__(
        self, 
        analysis_context: AnalysisContext, 
        session_context: SessionContext | None = None 
    ):
        self.analysis_context = analysis_context
        self.session_context = session_context

    def create(self) -> None:
        if shutil.which("curl") is None:
            raise ToolNotFoundException(
                "curl",
                "Install curl: https://curl.se/download.html"
            )

        if shutil.which("jq") is None:
            raise ToolNotFoundException(
                "jq",
                "Install jq: https://jqlang.org/download/",
            )

        if shutil.which("claude") is None:
            raise ToolNotFoundException(
                "claude",
                "Install Claude Code: https://code.claude.com/docs/en/",
            )

    def start(self) -> None:
        root = self.analysis_context.analysis_root
        pkg_manager = self.analysis_context.pkg_manager
        notebook_name = self.session_context.notebook_name
        notebook_port = self.session_context.notebook_port

        env = os.environ.copy()
        env.update(dotenv_values(root / ".env"))

        initial_prompt = f"/marimo-pair pair with me on {notebook_name} on port {notebook_port}"

        subprocess.Popen(
            [pkg_manager, *MARIMO_NOTEBOOK_EDIT_BASH, notebook_name, "--port" , notebook_port],
            cwd=root,
            env=env,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            [
                shutil.which("claude"), 
                "--model", CLAUDE_STARTUP_MODEL,
                "--effort",  CLAUDE_STARTUP_EFFORT,
                initial_prompt
            ],
            cwd=root,
            env=env,
            check=True,
        )
