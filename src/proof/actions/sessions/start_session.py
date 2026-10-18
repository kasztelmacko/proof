from pathlib import Path
from uuid import NAMESPACE_URL, uuid5
from proof.config import (
    MARIMO_NOTEBOOK_EDIT_BASH,
    MARIMO_NOTEBOOK_TOKEN,
)
import subprocess
import shutil
import time


def claude_session_id(session_name: str) -> str:
    return str(uuid5(NAMESPACE_URL, f"proof.agent_session.{session_name}"))


def start_notebook_session(
    analysis_root: Path,
    pkg_manager: str,
    notebook_name: str,
    notebook_port: str,
    env: dict[str, str],
) -> None:
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


def pair_with_notebook(
    analysis_root: Path,
    notebook_port: str,
    env: dict[str, str],
) -> str:
    notebook_url = f"http://localhost:{notebook_port}/"
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
    return pair_prompt.stdout.strip()


def start_agent_session(
    analysis_root: Path,
    notebook_port: str,
    env: dict[str, str],
    session_name: str,
    model: str,
    effort: str,
) -> None:
    pair_prompt = pair_with_notebook(
        analysis_root=analysis_root,
        notebook_port=notebook_port,
        env=env,
    )
    subprocess.run(
        [
            shutil.which("claude"),
            "--session-id", claude_session_id(session_name),
            "--agent", "harness",
            "--model", model,
            "--effort", effort,
            pair_prompt,
        ],
        cwd=analysis_root,
        env=env,
        check=True,
    )


def resume_agent_session(
    analysis_root: Path,
    notebook_port: str,
    env: dict[str, str],
    session_name: str,
    model: str,
    effort: str,
) -> None:
    pair_prompt = pair_with_notebook(
        analysis_root=analysis_root,
        notebook_port=notebook_port,
        env=env,
    )
    subprocess.run(
        [
            shutil.which("claude"),
            "--resume", claude_session_id(session_name),
            "--agent", "harness",
            "--model", model,
            "--effort", effort,
            pair_prompt,
        ],
        cwd=analysis_root,
        env=env,
        check=True,
    )
