from dataclasses import dataclass

AGENT_NAMES = ("harness", "planner", "coder", "summarizer")
EFFORT_LEVELS = ("low", "medium", "high", "xhigh", "max")
AGENT_TOOL_NAMES = ("claude", "codex", "opencode")


@dataclass(frozen=True)
class ModelSpec:
    model: str
    version: str
    effort: str


@dataclass(frozen=True)
class AgentToolConfig:
    name: str
    binary: str
    install_hint: str
    dest_dir: str
    env_var: str
    pair_flag: str | None
    skills_dir: str
    agents_dir: str | None
    default_models: dict[str, ModelSpec]


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


TOOL_CONFIGS: dict[str, AgentToolConfig] = {
    "claude": AgentToolConfig(
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
    "codex": AgentToolConfig(
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
    "opencode": AgentToolConfig(
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
