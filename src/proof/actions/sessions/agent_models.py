import re
import tomllib
from pathlib import Path

from proof.actions.context import AgentModel
from proof.config import (
    AGENT_NAMES,
    CLAUDE_AGENTS_PATH,
    DEFAULT_AGENT_MODELS,
    EFFORT_LEVELS,
    PROOF_CONFIG_FILE_NAME,
    PROOF_FILE_PATH,
)
from proof.exceptions import AgentConfigException


def default_agents_toml() -> str:
    lines: list[str] = []
    for name in AGENT_NAMES:
        spec = DEFAULT_AGENT_MODELS[name]
        lines.append(f"[agents.{name}]")
        lines.append(f'model = "{spec["model"]}"')
        lines.append(f'version = "{spec["version"]}"')
        lines.append(f'effort = "{spec["effort"]}"')
        lines.append("")
    return "\n".join(lines)


def load_agent_models(project_root: Path) -> dict[str, AgentModel]:
    path = project_root / PROOF_FILE_PATH / PROOF_CONFIG_FILE_NAME
    loaded: dict = {}
    if path.is_file():
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
        loaded = parsed

    agents = loaded.get("agents", {})
    if not isinstance(agents, dict):
        raise AgentConfigException("[agents] must be a table.")

    models: dict[str, AgentModel] = {}
    for name in AGENT_NAMES:
        default = DEFAULT_AGENT_MODELS[name]
        entry = agents.get(name, {})
        if not isinstance(entry, dict):
            raise AgentConfigException(f"[agents.{name}] must be a table.")

        model = entry.get("model", default["model"])
        version = entry.get("version", default["version"])
        effort = entry.get("effort", default["effort"])
        if not all(isinstance(value, str) for value in (model, version, effort)):
            raise AgentConfigException(
                f"[agents.{name}] model, version, and effort must be strings."
            )

        model = model.strip()
        version = version.strip()
        if not model:
            raise AgentConfigException(f"[agents.{name}] model is empty.")
        if effort not in EFFORT_LEVELS:
            allowed = ", ".join(EFFORT_LEVELS)
            raise AgentConfigException(
                f"[agents.{name}] effort must be one of: {allowed}."
            )

        model_id = model if not version else f"{model}-{version}"
        models[name] = AgentModel(model_id=model_id, effort=effort)
    return models


def apply_agent_models(analysis_root: Path, models: dict[str, AgentModel]) -> None:
    frontmatter = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
    for name in AGENT_NAMES:
        path = analysis_root / CLAUDE_AGENTS_PATH / f"{name}.md"
        if not path.is_file():
            raise AgentConfigException(
                f"Agent file for [cyan]{name}[/cyan] was not found. "
                "Copy the current .claude tree into this analysis."
            )

        text = path.read_text(encoding="utf-8")
        match = frontmatter.match(text)
        if not match:
            raise AgentConfigException(
                f"Agent file for [cyan]{name}[/cyan] is missing frontmatter."
            )

        spec = models[name]
        front, model_count = re.subn(
            r"^model:.*$",
            f"model: {spec.model_id}",
            match.group(1),
            count=1,
            flags=re.M,
        )
        front, effort_count = re.subn(
            r"^effort:.*$", f"effort: {spec.effort}", front, count=1, flags=re.M
        )
        if model_count != 1 or effort_count != 1:
            raise AgentConfigException(
                f"Agent file for [cyan]{name}[/cyan] is missing model or effort."
            )
        path.write_text(f"---\n{front}\n---\n{text[match.end() :]}", encoding="utf-8")
