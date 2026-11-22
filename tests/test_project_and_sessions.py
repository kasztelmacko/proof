import json
from pathlib import Path

import pytest

from proof.actions.context import AgentModel
from proof.actions.sessions.agent_models import (
    load_agent_models,
    load_agent_tool_name,
)
from proof.actions.sessions.manage_session import read_sessions
from proof.actions.sessions.project_files import project_agent_files
from proof.actions.sessions.start_session import build_session_env
from proof.agent_tools import agent_session_id, get_tool
from proof.config import MARIMO_NOTEBOOK_TOKEN
from proof.exceptions import AgentConfigException


def _models(tool_name: str) -> dict[str, AgentModel]:
    tool = get_tool(tool_name)
    return {
        name: AgentModel(model_id=tool.model_id(spec), effort=spec.effort)
        for name, spec in tool.default_models.items()
    }


def test_claude_projection_rewrites_model_frontmatter(tmp_path: Path) -> None:
    project_agent_files(tmp_path, get_tool("claude"), _models("claude"))

    harness = (tmp_path / ".claude" / "agents" / "harness.md").read_text(
        encoding="utf-8"
    )
    skill = tmp_path / ".claude" / "skills" / "marimo-pair" / "SKILL.md"
    settings = (tmp_path / ".claude" / "settings.json").read_text(encoding="utf-8")

    assert "model: claude-opus-4-6" in harness
    assert "effort: medium" in harness
    assert skill.is_file()
    assert "CLAUDE_CODE_DISABLE_BACKGROUND_TASKS" in settings


def test_codex_projection_writes_skills_agents_and_config(tmp_path: Path) -> None:
    project_agent_files(tmp_path, get_tool("codex"), _models("codex"))

    skill = tmp_path / ".codex" / "skills" / "marimo-pair" / "SKILL.md"
    config = (tmp_path / ".codex" / "config.toml").read_text(encoding="utf-8")
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")

    assert skill.is_file()
    assert 'model = "gpt-6.1-sol"' in config
    assert 'model_reasoning_effort = "medium"' in config
    assert agents.startswith("# harness")
    assert "You are the session harness." in agents
    assert "# planner" in agents


def test_opencode_projection_writes_agents_and_model(tmp_path: Path) -> None:
    project_agent_files(tmp_path, get_tool("opencode"), _models("opencode"))

    harness = (tmp_path / ".opencode" / "agents" / "harness.md").read_text(
        encoding="utf-8"
    )
    planner = (tmp_path / ".opencode" / "agents" / "planner.md").read_text(
        encoding="utf-8"
    )
    config = (tmp_path / ".opencode" / "opencode.jsonc").read_text(encoding="utf-8")
    skill = tmp_path / ".opencode" / "skills" / "marimo-pair" / "SKILL.md"

    assert "mode: primary" in harness
    assert "model: anthropic/claude-opus-4-6#medium" in harness
    assert "mode: subagent" in planner
    assert "model: anthropic/claude-opus-5-5#medium" in planner
    assert '"model": "anthropic/claude-opus-4-6"' in config
    assert skill.is_file()


def test_switching_tool_projects_the_other_layout(tmp_path: Path) -> None:
    project_agent_files(tmp_path, get_tool("claude"), _models("claude"))
    project_agent_files(tmp_path, get_tool("opencode"), _models("opencode"))

    assert (tmp_path / ".claude" / "agents" / "harness.md").is_file()
    assert (tmp_path / ".opencode" / "agents" / "harness.md").is_file()


def test_legacy_session_list_migrates_to_analysis_sessions(tmp_path: Path) -> None:
    legacy = tmp_path / ".claude"
    legacy.mkdir()
    (legacy / "sessions.json").write_text(
        json.dumps(["explore"]) + "\n", encoding="utf-8"
    )

    sessions = read_sessions(tmp_path)

    assert sessions == {"explore": agent_session_id("explore")}
    stored = json.loads((tmp_path / "sessions.json").read_text(encoding="utf-8"))
    assert stored["explore"]["id"] == agent_session_id("explore")


def test_load_models_uses_selected_tool_and_falls_back(tmp_path: Path) -> None:
    proof = tmp_path / ".proof"
    proof.mkdir()
    (proof / "proof.toml").write_text(
        'pkg_manager = "uv"\nagent_tool = "codex"\n',
        encoding="utf-8",
    )

    assert load_agent_tool_name(tmp_path) == "codex"
    models = load_agent_models(tmp_path)
    assert models["harness"].model_id == "gpt-6.1-sol"
    assert models["harness"].effort == "medium"


def test_unknown_agent_tool_in_config_is_rejected(tmp_path: Path) -> None:
    proof = tmp_path / ".proof"
    proof.mkdir()
    (proof / "proof.toml").write_text(
        'agent_tool = "cursor"\n',
        encoding="utf-8",
    )

    with pytest.raises(AgentConfigException):
        load_agent_tool_name(tmp_path)


def test_empty_dotenv_values_do_not_override_login(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    proof = tmp_path / ".proof"
    proof.mkdir()
    (proof / ".env").write_text(
        "ANTHROPIC_API_KEY=\nOPENAI_API_KEY=sk-test\n",
        encoding="utf-8",
    )
    analysis = tmp_path / "analysis"
    analysis.mkdir()
    (analysis / ".env").write_text("OPENCODE_API_KEY=oc-test\n", encoding="utf-8")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "from-login")

    env = build_session_env(tmp_path, analysis)

    assert env["ANTHROPIC_API_KEY"] == "from-login"
    assert env["OPENAI_API_KEY"] == "sk-test"
    assert env["OPENCODE_API_KEY"] == "oc-test"
    assert env["MARIMO_TOKEN"] == MARIMO_NOTEBOOK_TOKEN
