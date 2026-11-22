import shutil
import subprocess
from pathlib import Path

import pytest
from typer.testing import CliRunner

from proof.agent_tools import agent_session_id
from proof.cli import app
from proof.commands import (
    add_notebook,
    add_symlink,
    create_analysis,
    resume_session,
    start_session,
)

runner = CliRunner()


def _fake_which(name: str) -> str:
    return f"/usr/bin/{name}"


def _install_recorder(calls: list[list[str]]):
    def fake_run(args, **kwargs):
        calls.append(list(args))
        return subprocess.CompletedProcess(args, 0)

    return fake_run


def test_init_writes_config_and_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "uv.lock").write_text("", encoding="utf-8")
    monkeypatch.setattr(shutil, "which", _fake_which)
    calls: list[list[str]] = []
    monkeypatch.setattr(subprocess, "run", _install_recorder(calls))

    result = runner.invoke(app, ["init", "--agent", "codex"])

    assert result.exit_code == 0, result.output
    config = (tmp_path / ".proof" / "proof.toml").read_text(encoding="utf-8")
    env = (tmp_path / ".proof" / ".env").read_text(encoding="utf-8")
    assert 'agent_tool = "codex"' in config
    assert "[tools.claude.agents.harness]" in config
    assert "[tools.codex.agents.harness]" in config
    assert "[tools.opencode.agents.summarizer]" in config
    assert "ANTHROPIC_API_KEY=" in env
    assert "OPENAI_API_KEY=" in env
    assert "OPENCODE_API_KEY=" in env
    assert "CURSOR_API_KEY" not in env
    assert any("marimo>=0.23.15" in arg for command in calls for arg in command)


def test_init_keeps_existing_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "uv.lock").write_text("", encoding="utf-8")
    proof = tmp_path / ".proof"
    proof.mkdir()
    (proof / ".env").write_text("OPENAI_API_KEY=keep-me\n", encoding="utf-8")
    monkeypatch.setattr(shutil, "which", _fake_which)
    monkeypatch.setattr(subprocess, "run", _install_recorder([]))

    result = runner.invoke(app, ["init", "--agent", "claude"])

    assert result.exit_code == 0, result.output
    assert (proof / ".env").read_text(encoding="utf-8") == "OPENAI_API_KEY=keep-me\n"


def test_init_requires_agent() -> None:
    result = runner.invoke(app, ["init"])

    assert result.exit_code != 0


def test_init_missing_binary_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "uv.lock").write_text("", encoding="utf-8")

    def which(name: str) -> str | None:
        if name == "codex":
            return None
        return f"/usr/bin/{name}"

    monkeypatch.setattr(shutil, "which", which)

    result = runner.invoke(app, ["init", "--agent", "codex"])

    assert result.exit_code == 1
    assert "codex" in (result.stdout + result.stderr + result.output)


def _prepare_project(tmp_path: Path, agent_tool: str = "claude") -> None:
    from proof.agent_tools import render_proof_toml

    (tmp_path / "uv.lock").write_text("", encoding="utf-8")
    proof = tmp_path / ".proof"
    proof.mkdir()
    (proof / "CONTEXT.md").touch()
    (proof / "proof.toml").write_text(
        render_proof_toml("uv", agent_tool),
        encoding="utf-8",
    )


def test_create_projects_claude_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_project(tmp_path, "claude")

    create_analysis("prices")

    analysis = tmp_path / ".proof" / "prices"
    harness = (analysis / ".claude" / "agents" / "harness.md").read_text(
        encoding="utf-8"
    )
    assert "model: claude-opus-4-6" in harness
    assert (analysis / ".claude" / "skills" / "marimo-pair" / "SKILL.md").is_file()
    assert (analysis / "notebook.py").is_file()
    assert not (analysis / ".env").exists()


def test_create_follows_config_when_tool_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_project(tmp_path, "claude")
    create_analysis("first")

    config = tmp_path / ".proof" / "proof.toml"
    config.write_text(
        config.read_text(encoding="utf-8").replace(
            'agent_tool = "claude"',
            'agent_tool = "codex"',
        ),
        encoding="utf-8",
    )
    create_analysis("second")

    analysis = tmp_path / ".proof" / "second"
    assert (analysis / ".codex" / "skills" / "marimo-pair" / "SKILL.md").is_file()
    assert "You are the session harness." in (analysis / "AGENTS.md").read_text(
        encoding="utf-8"
    )

    config.write_text(
        config.read_text(encoding="utf-8").replace(
            'agent_tool = "codex"',
            'agent_tool = "opencode"',
        ),
        encoding="utf-8",
    )
    create_analysis("third")
    harness = (
        tmp_path / ".proof" / "third" / ".opencode" / "agents" / "harness.md"
    ).read_text(encoding="utf-8")
    assert "mode: primary" in harness


def test_add_notebook_and_symlink(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_project(tmp_path)
    create_analysis("prices")
    (tmp_path / "data.csv").write_text("a,b\n", encoding="utf-8")

    add_notebook("prices", "extra")
    add_symlink("prices", "data.csv")

    analysis = tmp_path / ".proof" / "prices"
    assert (analysis / "extra.py").is_file()
    assert (analysis / "analysis_context" / "data.csv").exists()


def test_missing_analysis_notebook_and_session_exit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)

    assert (
        runner.invoke(app, ["start", "prices", "notebook.py", "explore"]).exit_code == 1
    )

    _prepare_project(tmp_path)
    assert (
        runner.invoke(app, ["start", "prices", "notebook.py", "explore"]).exit_code == 1
    )

    create_analysis("prices")
    missing_notebook = runner.invoke(app, ["start", "prices", "notebook", "explore"])
    assert missing_notebook.exit_code == 1

    missing_session = runner.invoke(app, ["resume", "prices", "notebook.py", "explore"])
    assert missing_session.exit_code == 1


def test_start_and_resume_pass_the_agent_prompt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    _prepare_project(tmp_path, "claude")
    create_analysis("prices")
    prompt = "http://localhost:8080/ pair"

    monkeypatch.setattr(
        "proof.actions.run_bash_commands.start_notebook_session",
        lambda **kwargs: object(),
    )
    monkeypatch.setattr(
        "proof.actions.sessions.start_session.pair_with_notebook",
        lambda **kwargs: prompt,
    )
    monkeypatch.setattr(
        "proof.actions.sessions.start_session.shutil.which",
        lambda name: f"/bin/{name}",
    )
    captured: list[list[str]] = []

    def fake_run(args, **kwargs):
        captured.append(list(args))
        return subprocess.CompletedProcess(args, 0)

    monkeypatch.setattr("proof.actions.sessions.start_session.subprocess.run", fake_run)

    start_session("prices", "notebook.py", "explore")
    resume_session("prices", "notebook.py", "explore")

    assert captured[0][-1] == prompt
    assert captured[0][1:3] == ["--session-id", agent_session_id("explore")]
    assert "--resume" not in captured[0]
    assert captured[1][-1] == prompt
    assert captured[1][1:3] == ["--resume", agent_session_id("explore")]
    assert "--session-id" not in captured[1]
