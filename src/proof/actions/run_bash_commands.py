from proof.actions import ProjectContext, AnalysisContext, SessionContext
from proof.config import (
    MARIMO_NOTEBOOK_EDIT_BASH,
    MARIMO_NOTEBOOK_TOKEN,
    CLAUDE_STARTUP_MODEL,
    CLAUDE_STARTUP_EFFORT
)
from proof.errors import ToolNotFoundException
import subprocess
import shutil
import os
import time
from dotenv import dotenv_values

class RunBashCommands():
    def __init__(
        self,
        project_context: ProjectContext,
        analysis_context: AnalysisContext | None = None,
        session_context: SessionContext | None = None,
    ):
        self.project_context = project_context
        self.analysis_context = analysis_context
        self.session_context = session_context

    def init(self) -> None:
        if shutil.which("curl") is None:
            raise ToolNotFoundException(
                tool_name="curl",
                install_hint="Install curl: https://curl.se/download.html"
            )

        if shutil.which("jq") is None:
            raise ToolNotFoundException(
                tool_name="jq",
                install_hint="Install jq: https://jqlang.org/download/",
            )

        if shutil.which("uvx") is None:
            raise ToolNotFoundException(
                tool_name="uvx",
                install_hint="Install uv: https://docs.astral.sh/uv/getting-started/installation/",
            )

        if shutil.which("claude") is None:
            raise ToolNotFoundException(
                tool_name="claude",
                install_hint="Install Claude Code: https://code.claude.com/docs/en/",
            )

    def start(self) -> None:
        analysis_root = self.analysis_context.analysis_root
        pkg_manager = self.project_context.pkg_manager
        notebook_name = self.session_context.notebook_name
        notebook_port = self.session_context.notebook_port
        notebook_url = f"http://localhost:{notebook_port}/"

        env = os.environ.copy()
        env.update(dotenv_values(analysis_root / ".env"))
        env["MARIMO_TOKEN"] = MARIMO_NOTEBOOK_TOKEN

        subprocess.Popen(
            [
                pkg_manager,
                *MARIMO_NOTEBOOK_EDIT_BASH,
                notebook_name,
                "--port",
                notebook_port,
                "--token-password",
                MARIMO_NOTEBOOK_TOKEN,
            ],
            cwd=analysis_root,
            env=env,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        sessions_url = f"http://127.0.0.1:{notebook_port}/api/sessions"
        while True:
            sessions_response = subprocess.run(
                [
                    "curl",
                    "-sf",
                    "--connect-timeout",
                    "1",
                    "--max-time",
                    "2",
                    "-H",
                    f"Authorization: Bearer {MARIMO_NOTEBOOK_TOKEN}",
                    sessions_url,
                ],
                capture_output=True,
                text=True,
            )
            if sessions_response.returncode == 0:
                session_id = subprocess.run(
                    ["jq", "-r", "keys[0] // empty"],
                    input=sessions_response.stdout,
                    capture_output=True,
                    text=True,
                ).stdout.strip()
                if session_id:
                    break
            time.sleep(0.5)

        pair_prompt = subprocess.run(
            [
                shutil.which("uvx"),
                "marimo@latest",
                "pair",
                "prompt",
                "--url",
                notebook_url,
                "--session",
                session_id,
                "--with-token",
                "--claude",
            ],
            cwd=analysis_root,
            env=env,
            capture_output=True,
            text=True,
            input="\n",
            check=True,
        )

        subprocess.run(
            [
                shutil.which("claude"),
                "--model", CLAUDE_STARTUP_MODEL,
                "--effort",  CLAUDE_STARTUP_EFFORT,
                pair_prompt.stdout.strip(),
            ],
            cwd=analysis_root,
            env=env,
            check=True,
        )
