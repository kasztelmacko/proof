from typing import Literal

PkgManager = Literal["poetry", "uv", "pip", "conda"]
ModelsCLI = Literal["claude", "cursor", "copilot"]

PROOF_CONFIG_FILE_NAME = "proof.toml"
DEFAULT_NOTEBOOK_FILE_NAME = "notebook"


REQUIRED_DEPENDENCIES = ("marimo>=0.23.15",)
PACKAGE_MANAGER_INDICATORS = {
    ("poetry.lock",) : "poetry",
    ("uv.lock",): "uv",
    ("environment.yml", "environment.yaml", "conda-lock.yml"): "conda",
    ("requirements.txt", "requirements-dev.txt", "setup.py", "setup.cfg"): "pip"
} 
