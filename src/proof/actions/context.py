from dataclasses import dataclass
from pathlib import Path


@dataclass
class AnalysisContext:
    analysis_name: str
    project_root: Path
    analysis_root: Path
    pkg_manager: str