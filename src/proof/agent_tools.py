from dataclasses import dataclass
from uuid import NAMESPACE_URL, uuid5

from proof.exceptions import AgentConfigException

AGENT_NAMES = ("harness", "planner", "coder", "summarizer")
EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")
AGENT_TOOL_NAMES = ("claude", "codex", "opencode")


@dataclass(frozen=True)
class ModelSpec:
    model: str
    version: str
    effort: str


def _uniform(model: str, version: str, effort: str) -> dict[str, ModelSpec]:
    return {name: ModelSpec(model, version, effort) for name in AGENT_NAMES}


CLAUDE_DEFAULT_MODELS = {
    "harness": ModelSpec("claude-opus", "4-6", "medium"),
    "planner": ModelSpec("claude-opus", "5-5", "medium"),
    "coder": ModelSpec("claude-opus", "4-8", "medium"),
    "summarizer": ModelSpec("claude-opus", "5-5", "medium"),
}
CODEX_DEFAULT_MODELS = _uniform("gpt-6.1-sol", "", "medium")
OPENCODE_DEFAULT_MODELS = {
    "harness": ModelSpec("anthropic/claude-opus-4-6", "", "medium"),
    "planner": ModelSpec("anthropic/claude-opus-5-5", "", "medium"),
    "coder": ModelSpec("anthropic/claude-opus-4-8", "", "medium"),
    "summarizer": ModelSpec("anthropic/claude-opus-5-5", "", "medium"),
}


@dataclass(frozen=True)
class AgentTool:
    name: str
    binary: str
    install_hint: str
    dest_dir: str
    env_var: str
    pair_flag: str | None
    skills_dir: str
    agents_dir: str | None
    default_models: dict[str, ModelSpec]

    def model_id(self, spec: ModelSpec) -> str:
        if self.name == "claude" and spec.version:
            return f"{spec.model}-{spec.version}"
        return spec.model

    def start_command(
        self,
        *,
        binary_path: str,
        session_id: str,
        model_id: str,
        effort: str,
        prompt: str,
    ) -> list[str]:
        if self.name == "claude":
            return [
                binary_path,
                "--session-id",
                session_id,
                "--agent",
                "harness",
                "--model",
                model_id,
                "--effort",
                effort,
                prompt,
            ]
        if self.name == "codex":
            return [
                binary_path,
                "--model",
                model_id,
                "-c",
                f"model_reasoning_effort={effort}",
                prompt,
            ]
        return [
            binary_path,
            "--agent",
            "harness",
            "--model",
            model_id,
            "--prompt",
            prompt,
        ]

    def resume_command(
        self,
        *,
        binary_path: str,
        session_id: str,
        model_id: str,
        effort: str,
        prompt: str,
    ) -> list[str]:
        if self.name == "claude":
            return [
                binary_path,
                "--resume",
                session_id,
                "--agent",
                "harness",
                "--model",
                model_id,
                "--effort",
                effort,
                prompt,
            ]
        if self.name == "codex":
            return [
                binary_path,
                "--model",
                model_id,
                "-c",
                f"model_reasoning_effort={effort}",
                "resume",
                session_id,
                prompt,
            ]
        return [
            binary_path,
            "--session",
            session_id,
            "--agent",
            "harness",
            "--model",
            model_id,
            "--prompt",
            prompt,
        ]


TOOLS: dict[str, AgentTool] = {
    "claude": AgentTool(
        name="claude",
        binary="claude",
        install_hint="Install Claude Code: https://code.claude.com/docs/en/",
        dest_dir=".claude",
        env_var="ANTHROPIC_API_KEY",
        pair_flag="--claude",
        skills_dir=".claude/skills",
        agents_dir=".claude/agents",
        default_models=CLAUDE_DEFAULT_MODELS,
    ),
    "codex": AgentTool(
        name="codex",
        binary="codex",
        install_hint="Install Codex CLI: https://developers.openai.com/codex/cli/",
        dest_dir=".codex",
        env_var="OPENAI_API_KEY",
        pair_flag="--codex",
        skills_dir=".codex/skills",
        agents_dir=None,
        default_models=CODEX_DEFAULT_MODELS,
    ),
    "opencode": AgentTool(
        name="opencode",
        binary="opencode",
        install_hint="Install OpenCode: https://opencode.ai/docs/",
        dest_dir=".opencode",
        env_var="OPENCODE_API_KEY",
        pair_flag="--opencode",
        skills_dir=".opencode/skills",
        agents_dir=".opencode/agents",
        default_models=OPENCODE_DEFAULT_MODELS,
    ),
}


def get_tool(name: str) -> AgentTool:
    try:
        return TOOLS[name]
    except KeyError as exc:
        allowed = ", ".join(AGENT_TOOL_NAMES)
        raise AgentConfigException(f"agent_tool must be one of: {allowed}.") from exc


def agent_session_id(session_name: str) -> str:
    return str(uuid5(NAMESPACE_URL, f"proof.agent_session.{session_name}"))


def allocate_session_id(tool: AgentTool, session_name: str) -> str:
    if tool.name == "codex":
        return session_name
    return agent_session_id(session_name)


def command_session_id(tool: AgentTool, session_name: str, stored: str | None) -> str:
    if tool.name == "codex":
        return session_name
    if stored:
        return stored
    return agent_session_id(session_name)


def render_proof_toml(pkg_manager: str, agent_tool: str) -> str:
    get_tool(agent_tool)
    lines = [
        f'pkg_manager = "{pkg_manager}"',
        f'agent_tool = "{agent_tool}"',
        "",
    ]
    for tool_name in AGENT_TOOL_NAMES:
        tool = TOOLS[tool_name]
        for role in AGENT_NAMES:
            spec = tool.default_models[role]
            lines.append(f"[tools.{tool_name}.agents.{role}]")
            lines.append(f'model = "{spec.model}"')
            lines.append(f'version = "{spec.version}"')
            lines.append(f'effort = "{spec.effort}"')
            lines.append("")
    return "\n".join(lines)
