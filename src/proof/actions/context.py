from dataclasses import dataclass
from pathlib import Path
from proof.config import ModelsCLI


@dataclass
class AnalysisContext:
    analysis_name: str
    project_root: Path
    analysis_root: Path
    pkg_manager: str

@dataclass
class SessionContext:
    model_cli: ModelsCLI
    notebook_name: str