import json
from pathlib import Path

from proof.agent_tools import agent_session_id
from proof.exceptions import SessionNotFoundException

SESSIONS_FILE_NAME = "sessions.json"
LEGACY_SESSIONS_PATH = Path(".claude") / "sessions.json"


def sessions_file(analysis_root: Path) -> Path:
    return analysis_root / SESSIONS_FILE_NAME


def require_session_exists(
    analysis_root: Path, analysis_name: str, session_name: str
) -> None:
    if session_name not in read_sessions(analysis_root):
        raise SessionNotFoundException(
            session_name=session_name,
            analysis_name=analysis_name,
        )


def read_sessions(analysis_root: Path) -> dict[str, str]:
    path = sessions_file(analysis_root)
    if path.is_file():
        return _parse_sessions(path.read_text(encoding="utf-8"), legacy_list=False)

    legacy = analysis_root / LEGACY_SESSIONS_PATH
    if not legacy.is_file():
        return {}

    sessions = _parse_sessions(legacy.read_text(encoding="utf-8"), legacy_list=True)
    if sessions:
        write_sessions(analysis_root, sessions)
    return sessions


def write_sessions(analysis_root: Path, sessions: dict[str, str]) -> None:
    path = sessions_file(analysis_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {name: {"id": session_id} for name, session_id in sessions.items()}
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _parse_sessions(text: str, *, legacy_list: bool) -> dict[str, str]:
    data = json.loads(text)
    if isinstance(data, list):
        return {name: agent_session_id(name) for name in data if isinstance(name, str)}
    if not isinstance(data, dict):
        return {}
    if legacy_list:
        return {}

    sessions: dict[str, str] = {}
    for name, entry in data.items():
        if not isinstance(name, str):
            continue
        if isinstance(entry, dict) and isinstance(entry.get("id"), str):
            sessions[name] = entry["id"]
        elif isinstance(entry, str):
            sessions[name] = entry
    return sessions
