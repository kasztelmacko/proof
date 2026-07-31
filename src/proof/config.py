from typing import Literal
from pathlib import Path

PROOF_CONFIG_FILE_NAME = "proof.toml"
PROOF_TEMPLATES_PATH = "templates"

PI_AGENT_PATH = Path("pi") / "agent"
PI_AGENT_AUTH_FILE_NAME = "auth.json"

CONTEXT_FILE_PATH = Path("context")
NOTES_FILE_PATH = Path("notes")

DEFAULT_NOTEBOOK_FILE_NAME = "notebook"


PkgManager = Literal["poetry", "uv", "pip", "conda"]
PACKAGE_MANAGER_INDICATORS = {
    ("poetry.lock",) : "poetry",
    ("uv.lock",): "uv",
    ("environment.yml", "environment.yaml", "conda-lock.yml"): "conda",
    ("requirements.txt", "requirements-dev.txt", "setup.py", "setup.cfg"): "pip"
} 

REQUIRED_DEPENDENCIES = ("marimo>=0.23.15",)

MARIMO_NOTEBOOK_EDIT_BASH = ["run", "marimo", "edit", "--watch"]