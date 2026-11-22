import os
import shutil
import subprocess
import time
from pathlib import Path

from dotenv import dotenv_values

from proof.agent_tools import AgentTool
from proof.config import (
    MARIMO_NOTEBOOK_EDIT_BASH,
    MARIMO_NOTEBOOK_TOKEN,
    NOTEBOOK_READY_SECONDS,
    PROOF_DOTENV_FILE_NAME,
    PROOF_FILE_PATH,
)
from proof.exceptions import NotebookTimeoutException, ToolNotFoundException


def build_session_env(project_root: Path, analysis_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    _overlay_dotenv(env, project_root / PROOF_FILE_PATH / PROOF_DOTENV_FILE_NAME)
    _overlay_dotenv(env, analysis_root / ".env")
    env["MARIMO_TOKEN"] = MARIMO_NOTEBOOK_TOKEN
    return env


def _overlay_dotenv(env: dict[str, str], path: Path) -> None:
    if not path.is_file():
        return
    for key, value in dotenv_values(path).items():
        if value and value.strip():
            env[key] = value


def start_notebook_session(
    analysis_root: Path,
    pkg_manager: str,
    notebook_name: str,
    notebook_port: str,
    env: dict[str, str],
) -> subprocess.Popen:
    return subprocess.Popen(
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


def pair_with_notebook(
    analysis_root: Path,
    notebook_port: str,
    env: dict[str, str],
    pair_flag: str | None,
) -> str:
    notebook_url = f"http://localhost:{notebook_port}/"
    sessions_url = f"http://127.0.0.1:{notebook_port}/api/sessions"
    deadline = time.monotonic() + NOTEBOOK_READY_SECONDS
    session_id = ""
    while time.monotonic() < deadline:
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
    if not session_id:
        raise NotebookTimeoutException()

    command = [
        shutil.which("uvx"),
        "marimo@latest",
        "pair",
        "prompt",
        "--url",
        notebook_url,
        "--session",
        session_id,
        "--with-token",
    ]
    if pair_flag:
        command.append(pair_flag)
    pair_prompt = subprocess.run(
        command,
        cwd=analysis_root,
        env=env,
        capture_output=True,
        text=True,
        input="\n",
        check=True,
    )
    return pair_prompt.stdout.strip()


def run_agent_process(
    *,
    analysis_root: Path,
    notebook_port: str,
    env: dict[str, str],
    tool: AgentTool,
    session_id: str,
    model_id: str,
    effort: str,
    resume: bool,
    has_stored_id: bool,
) -> None:
    prompt = pair_with_notebook(
        analysis_root=analysis_root,
        notebook_port=notebook_port,
        env=env,
        pair_flag=tool.pair_flag,
    )
    binary = shutil.which(tool.binary)
    if binary is None:
        raise ToolNotFoundException(
            tool_name=tool.binary, install_hint=tool.install_hint
        )
    if resume and has_stored_id:
        argv = tool.resume_command(
            binary_path=binary,
            session_id=session_id,
            model_id=model_id,
            effort=effort,
            prompt=prompt,
        )
    else:
        argv = tool.start_command(
            binary_path=binary,
            session_id=session_id,
            model_id=model_id,
            effort=effort,
            prompt=prompt,
        )
    subprocess.run(argv, cwd=analysis_root, env=env, check=True)
