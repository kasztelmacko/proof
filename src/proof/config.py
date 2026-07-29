from typing import Literal

PkgManager = Literal["poetry", "uv", "pip", "conda"]
PACKAGE_MANAGER_INDICATORS = {
    ("poetry.lock") : "poetry",
    ("uv.lock"): "uv",
    ("environment.yml", "environment.yaml", "conda-lock.yml"): "conda",
    ("requirements.txt", "requirements-dev.txt", "setup.py", "setup.cfg"): "pip"
} 

ModelsCLI = Literal["claude", "cursor", "copilot"]