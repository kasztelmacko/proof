from typing import Literal
from pathlib import Path

PROOF_CONFIG_FILE_NAME = "proof.toml"
PROOF_ENV_FILE_NAME = ".env.example"
PROOF_COPY_FILES_PATH = "copy_files"

CLAUDE_AGENT_FILES_PATH = Path(".claude") 

CONTEXT_FILE_PATH = Path("context")
NOTES_FILE_PATH = Path("notes")
SKILLS_FILES_PATH = Path("skills")

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