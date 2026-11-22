import tomllib
from pathlib import Path

from proof.actions.context import AgentModel
from proof.agent_tools import get_tool
from proof.config import PROOF_CONFIG_FILE_NAME, PROOF_FILE_PATH
from proof.config.agent_config import AGENT_NAMES, EFFORT_LEVELS, ModelSpec
from proof.exceptions import AgentConfigException


def _read_config(project_root: Path) -> dict:
    path = project_root / PROOF_FILE_PATH / PROOF_CONFIG_FILE_NAME
    if not path.is_file():
        return {}
    try:
        with path.open("rb") as handle:
            parsed = tomllib.load(handle)
    except tomllib.TOMLDecodeError as exc:
        raise AgentConfigException(
            f"[cyan]{PROOF_CONFIG_FILE_NAME}[/cyan] could not be read: {exc}"
        ) from exc
    if not isinstance(parsed, dict):
        raise AgentConfigException(
            f"[cyan]{PROOF_CONFIG_FILE_NAME}[/cyan] must be a table."
        )
    return parsed


def load_agent_tool_name(project_root: Path) -> str:
    parsed = _read_config(project_root)
    name = parsed.get("agent_tool")
    if not isinstance(name, str):
        raise AgentConfigException(
            "agent_tool must be one of: claude, codex, opencode."
        )
    get_tool(name)
    return name


def load_agent_models(project_root: Path) -> dict[str, AgentModel]:
    parsed = _read_config(project_root)
    tool = get_tool(load_agent_tool_name(project_root))
    tools_table = parsed.get("tools", {})
    if not isinstance(tools_table, dict):
        raise AgentConfigException("[tools] must be a table.")
    tool_table = tools_table.get(tool.name, {})
    if not isinstance(tool_table, dict):
        raise AgentConfigException(f"[tools.{tool.name}] must be a table.")
    agents = tool_table.get("agents", {})
    if not isinstance(agents, dict):
        raise AgentConfigException(f"[tools.{tool.name}.agents] must be a table.")

    models: dict[str, AgentModel] = {}
    for name in AGENT_NAMES:
        default = tool.default_models[name]
        entry = agents.get(name, {})
        if not isinstance(entry, dict):
            raise AgentConfigException(
                f"[tools.{tool.name}.agents.{name}] must be a table."
            )
        model = entry.get("model", default.model)
        version = entry.get("version", default.version)
        effort = entry.get("effort", default.effort)
        if not all(isinstance(value, str) for value in (model, version, effort)):
            raise AgentConfigException(
                f"[tools.{tool.name}.agents.{name}] "
                "model, version, and effort must be strings."
            )
        model = model.strip()
        version = version.strip()
        if not model:
            raise AgentConfigException(
                f"[tools.{tool.name}.agents.{name}] model is empty."
            )
        if effort not in EFFORT_LEVELS:
            allowed = ", ".join(EFFORT_LEVELS)
            raise AgentConfigException(
                f"[tools.{tool.name}.agents.{name}] effort must be one of: {allowed}."
            )
        spec = ModelSpec(model=model, version=version, effort=effort)
        models[name] = AgentModel(model_id=tool.model_id(spec), effort=effort)
    return models
