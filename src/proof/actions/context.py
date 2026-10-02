from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectContext:
    project_root: Path
    pkg_manager: str

@dataclass
class AnalysisContext:
    analysis_name: str
    analysis_root: Path

@dataclass
class SessionContext:
    notebook_name: str
    notebook_port: str