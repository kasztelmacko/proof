from dataclasses import dataclass
from pathlib import Path


@dataclass
class AnalysisContext:
    analysis_name: str
    project_root: Path
    analysis_root: Path
    pkg_manager: str

@dataclass
class SessionContext:
    notebook_name: str
    notebook_port: str