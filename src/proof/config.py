from typing import Literal

PROOF_CONFIG_FILE_NAME = "proof.toml"
NOTEBOOK_FILE_NAME = "notebook.py"

PkgManager = Literal["poetry", "uv", "pip", "conda"]
PACKAGE_MANAGER_INDICATORS = {
    ("poetry.lock",) : "poetry",
    ("uv.lock",): "uv",
    ("environment.yml", "environment.yaml", "conda-lock.yml"): "conda",
    ("requirements.txt", "requirements-dev.txt", "setup.py", "setup.cfg"): "pip"
} 

ModelsCLI = Literal["claude", "cursor", "copilot"]