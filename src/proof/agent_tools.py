from dataclasses import dataclass
from uuid import NAMESPACE_URL, uuid5

from proof.config.agent_config import (
    AGENT_NAMES,
    AGENT_TOOL_NAMES,
    TOOL_CONFIGS,
    AgentToolConfig,
    ModelSpec,
)
from proof.exceptions import AgentConfigException


@dataclass(frozen=True)
class AgentTool(AgentToolConfig):
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
    name: AgentTool(**vars(config)) for name, config in TOOL_CONFIGS.items()
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
