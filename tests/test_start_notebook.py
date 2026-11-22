import shutil
import subprocess
from pathlib import Path

import pytest

from proof.commands import create_analysis, resume_session, start_session

pytestmark = pytest.mark.integration

MARIMO_NOTEBOOK = """import marimo

app = marimo.App()


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
"""


def _require_tools() -> None:
    missing = [
        name for name in ("curl", "jq", "uv", "uvx") if shutil.which(name) is None
    ]
    if missing:
        pytest.fail(f"Required tools are not on PATH: {', '.join(missing)}")


def _stop(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    subprocess.run(
        ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
        capture_output=True,
        check=False,
    )
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()


def _prepare_marimo_project(tmp_path: Path) -> None:
    subprocess.run(
        ["uv", "init", "--name", "fixture", "--python", "3.11"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["uv", "add", "marimo>=0.23.15"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    from proof.agent_tools import render_proof_toml

    proof = tmp_path / ".proof"
    proof.mkdir()
    (proof / "CONTEXT.md").touch()
    (proof / "proof.toml").write_text(
        render_proof_toml("uv", "claude"), encoding="utf-8"
    )
    (proof / ".env").write_text(
        "ANTHROPIC_API_KEY=\nOPENAI_API_KEY=\nOPENCODE_API_KEY=\n",
        encoding="utf-8",
    )


@pytest.fixture
def notebook_project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _require_tools()
    monkeypatch.chdir(tmp_path)
    for key in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "OPENCODE_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    _prepare_marimo_project(tmp_path)
    create_analysis("prices")
    notebook = tmp_path / ".proof" / "prices" / "notebook.py"
    notebook.write_text(MARIMO_NOTEBOOK, encoding="utf-8")

    captured: list[tuple[list[str], dict | None]] = []
    procs: list[subprocess.Popen] = []
    ports: list[str] = []
    real_which = shutil.which
    real_run = subprocess.run
    agent_binary = str(tmp_path / "claude.cmd")

    def which(name: str) -> str | None:
        if name == "claude":
            return agent_binary
        return real_which(name)

    def fake_run(args, **kwargs):
        if args and str(args[0]) == agent_binary:
            captured.append((list(args), kwargs.get("env")))
            return subprocess.CompletedProcess(args, 0, "", "")
        return real_run(args, **kwargs)

    real_start = __import__(
        "proof.actions.sessions.start_session", fromlist=["start_notebook_session"]
    ).start_notebook_session

    def spy(**kwargs):
        ports.append(kwargs["notebook_port"])
        proc = real_start(**kwargs)
        procs.append(proc)
        return proc

    monkeypatch.setattr(shutil, "which", which)
    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(
        "proof.actions.run_bash_commands.start_notebook_session",
        spy,
    )
    try:
        yield tmp_path, captured, procs, ports
    finally:
        for proc in procs:
            _stop(proc)


def test_start_boots_notebook_and_passes_prompt(notebook_project) -> None:
    _tmp_path, captured, procs, ports = notebook_project

    start_session("prices", "notebook.py", "explore")

    assert procs, "notebook process was not started"
    assert procs[0].poll() is None
    assert captured, "agent command was not invoked"
    argv, env = captured[0]
    assert f"http://localhost:{ports[0]}/" in argv[-1]
    assert env is not None
    assert not env.get("ANTHROPIC_API_KEY")
    assert not env.get("OPENAI_API_KEY")
    assert not env.get("OPENCODE_API_KEY")


def test_resume_passes_prompt_to_resume_command(notebook_project) -> None:
    _tmp_path, captured, procs, ports = notebook_project
    start_session("prices", "notebook.py", "explore")
    _stop(procs.pop())

    resume_session("prices", "notebook.py", "explore")

    assert procs[-1].poll() is None
    argv, _env = captured[-1]
    assert "--resume" in argv
    assert f"http://localhost:{ports[-1]}/" in argv[-1]
