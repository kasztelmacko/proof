import re
import shutil
from importlib.resources import as_file, files
from pathlib import Path

from proof.actions.context import AgentModel
from proof.agent_tools import AGENT_NAMES, AgentTool
from proof.config import PROOF_COPY_FILES_PATH
from proof.exceptions import AgentConfigException

_FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def project_agent_files(
    analysis_root: Path, tool: AgentTool, models: dict[str, AgentModel]
) -> None:
    canonical = files("proof").joinpath(PROOF_COPY_FILES_PATH, "agent")
    with as_file(canonical) as src:
        source = Path(src)
        if tool.name == "claude":
            _project_claude(analysis_root, source, models)
        elif tool.name == "codex":
            _project_codex(analysis_root, source, models)
        elif tool.name == "opencode":
            _project_opencode(analysis_root, source, models)
        else:
            raise AgentConfigException(f"No file layout for [cyan]{tool.name}[/cyan].")


def _project_claude(
    analysis_root: Path, source: Path, models: dict[str, AgentModel]
) -> None:
    dest = analysis_root / ".claude"
    _replace_tree(source, dest)
    _apply_claude_frontmatter(dest / "agents", models)


def _project_codex(
    analysis_root: Path, source: Path, models: dict[str, AgentModel]
) -> None:
    _replace_tree(source / "skills", analysis_root / ".codex" / "skills")
    harness = models["harness"]
    config_path = analysis_root / ".codex" / "config.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        f'model = "{harness.model_id}"\nmodel_reasoning_effort = "{harness.effort}"\n',
        encoding="utf-8",
    )
    _write_agents_md(analysis_root / "AGENTS.md", source / "agents")


def _project_opencode(
    analysis_root: Path, source: Path, models: dict[str, AgentModel]
) -> None:
    base = analysis_root / ".opencode"
    _replace_tree(source / "skills", base / "skills")
    agents_dest = base / "agents"
    if agents_dest.exists():
        shutil.rmtree(agents_dest)
    agents_dest.mkdir(parents=True)
    for name in AGENT_NAMES:
        text = (source / "agents" / f"{name}.md").read_text(encoding="utf-8")
        front, body = _split_frontmatter(text, name)
        description = _field(front, "description")
        mode = "primary" if name == "harness" else "subagent"
        spec = models[name]
        agents_dest.joinpath(f"{name}.md").write_text(
            "---\n"
            f"name: {name}\n"
            f"description: {description}\n"
            f"mode: {mode}\n"
            f"model: {spec.model_id}#{spec.effort}\n"
            "---\n"
            f"{body}",
            encoding="utf-8",
        )
    base.joinpath("opencode.jsonc").write_text(
        f'{{\n  "model": "{models["harness"].model_id}"\n}}\n',
        encoding="utf-8",
    )


def _replace_tree(source: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, dest)


def _apply_claude_frontmatter(agents_dir: Path, models: dict[str, AgentModel]) -> None:
    for name in AGENT_NAMES:
        path = agents_dir / f"{name}.md"
        if not path.is_file():
            raise AgentConfigException(
                f"Agent file for [cyan]{name}[/cyan] was not found. "
                "Project the agent files into this analysis."
            )
        text = path.read_text(encoding="utf-8")
        match = _FRONTMATTER.match(text)
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
            r"^effort:.*$",
            f"effort: {spec.effort}",
            front,
            count=1,
            flags=re.M,
        )
        if model_count != 1 or effort_count != 1:
            raise AgentConfigException(
                f"Agent file for [cyan]{name}[/cyan] is missing model or effort."
            )
        path.write_text(f"---\n{front}\n---\n{text[match.end() :]}", encoding="utf-8")


def _write_agents_md(path: Path, agents_dir: Path) -> None:
    parts: list[str] = []
    for name in AGENT_NAMES:
        text = (agents_dir / f"{name}.md").read_text(encoding="utf-8")
        _, body = _split_frontmatter(text, name)
        parts.append(f"# {name}\n\n{body.strip()}\n")
    path.write_text("\n".join(parts), encoding="utf-8")


def _split_frontmatter(text: str, name: str) -> tuple[str, str]:
    match = _FRONTMATTER.match(text)
    if not match:
        raise AgentConfigException(
            f"Agent file for [cyan]{name}[/cyan] is missing frontmatter."
        )
    return match.group(1), text[match.end() :]


def _field(front: str, field_name: str) -> str:
    match = re.search(rf"^{field_name}:\s*(.*)$", front, re.M)
    if not match:
        return ""
    return match.group(1).strip()
