import json
from pathlib import Path
from proof.config import CLAUDE_SESSIONS_FILE_PATH


def sessions_file(analysis_root: Path) -> Path:
    return analysis_root / CLAUDE_SESSIONS_FILE_PATH


def read_session_names(analysis_root: Path) -> list[str]:
    path = sessions_file(analysis_root)
    if not path.exists():
        return []

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return []
    return [name for name in data if isinstance(name, str)]


def write_session_names(analysis_root: Path, names: list[str]) -> None:
    path = sessions_file(analysis_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(names, indent=2) + "\n",
        encoding="utf-8",
    )
