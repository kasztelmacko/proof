import pytest

from proof.agent_tools import (
    TOOLS,
    ModelSpec,
    agent_session_id,
    get_tool,
    render_proof_toml,
)
from proof.exceptions import AgentConfigException


def test_claude_start_and_resume_commands() -> None:
    tool = get_tool("claude")
    prompt = "pair with the notebook"
    start = tool.start_command(
        binary_path="/bin/claude",
        session_id="session-1",
        model_id="claude-opus-4-6",
        effort="medium",
        prompt=prompt,
    )
    resume = tool.resume_command(
        binary_path="/bin/claude",
        session_id="session-1",
        model_id="claude-opus-4-6",
        effort="medium",
        prompt=prompt,
    )

    assert start == [
        "/bin/claude",
        "--session-id",
        "session-1",
        "--agent",
        "harness",
        "--model",
        "claude-opus-4-6",
        "--effort",
        "medium",
        prompt,
    ]
    assert resume[1:3] == ["--resume", "session-1"]
    assert "--session-id" not in resume
    assert resume[-1] == prompt


def test_codex_start_and_resume_commands() -> None:
    tool = get_tool("codex")
    prompt = "pair prompt"
    start = tool.start_command(
        binary_path="codex",
        session_id="explore",
        model_id="gpt-6.1-sol",
        effort="high",
        prompt=prompt,
    )
    resume = tool.resume_command(
        binary_path="codex",
        session_id="explore",
        model_id="gpt-6.1-sol",
        effort="high",
        prompt=prompt,
    )

    assert start == [
        "codex",
        "--model",
        "gpt-6.1-sol",
        "-c",
        "model_reasoning_effort=high",
        prompt,
    ]
    assert resume == [
        "codex",
        "--model",
        "gpt-6.1-sol",
        "-c",
        "model_reasoning_effort=high",
        "resume",
        "explore",
        prompt,
    ]


def test_opencode_start_and_resume_commands() -> None:
    tool = get_tool("opencode")
    prompt = "pair prompt"
    start = tool.start_command(
        binary_path="opencode",
        session_id="abc",
        model_id="anthropic/claude-sonnet-4-6",
        effort="medium",
        prompt=prompt,
    )
    resume = tool.resume_command(
        binary_path="opencode",
        session_id="abc",
        model_id="anthropic/claude-sonnet-4-6",
        effort="medium",
        prompt=prompt,
    )

    assert start == [
        "opencode",
        "--agent",
        "harness",
        "--model",
        "anthropic/claude-sonnet-4-6",
        "--prompt",
        prompt,
    ]
    assert resume[:4] == ["opencode", "--session", "abc", "--agent"]
    assert resume[-2:] == ["--prompt", prompt]


def test_model_ids_join_per_tool() -> None:
    claude = TOOLS["claude"].model_id(ModelSpec("claude-opus", "4-6", "medium"))
    codex = TOOLS["codex"].model_id(ModelSpec("gpt-6.1-sol", "", "medium"))
    opencode = TOOLS["opencode"].model_id(
        ModelSpec("anthropic/claude-sonnet-4-6", "", "medium")
    )

    assert claude == "claude-opus-4-6"
    assert codex == "gpt-6.1-sol"
    assert opencode == "anthropic/claude-sonnet-4-6"


def test_session_id_is_stable() -> None:
    assert agent_session_id("explore") == agent_session_id("explore")
    assert agent_session_id("explore") != agent_session_id("other")


def test_unknown_tool_is_rejected() -> None:
    with pytest.raises(AgentConfigException):
        get_tool("cursor")


def test_render_proof_toml_includes_every_tool() -> None:
    text = render_proof_toml("uv", "codex")

    assert 'agent_tool = "codex"' in text
    assert 'pkg_manager = "uv"' in text
    assert "[tools.claude.agents.harness]" in text
    assert "[tools.codex.agents.harness]" in text
    assert "[tools.opencode.agents.harness]" in text
    assert 'model = "gpt-6.1-sol"' in text
    assert 'model = "anthropic/claude-opus-4-6"' in text
