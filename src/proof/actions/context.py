from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectContext:
    project_root: Path
    pkg_manager: str

@dataclass(frozen=True)
class AnalysisContext:
    analysis_name: str
    analysis_root: Path

@dataclass(frozen=True)
class SessionContext:
    notebook_name: str
    notebook_port: str
    session_name: str

@dataclass(frozen=True)
class AgentModel:
    model_id: str
    effort: str