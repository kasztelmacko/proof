from typing import Literal
from pathlib import Path

PROOF_CONFIG_FILE_NAME = "proof.toml"
PROOF_ENV_FILE_NAME = ".env.example"
PROOF_COPY_FILES_PATH = "copy_files"
PROOF_FILE_PATH = ".proof"
PROOF_PROJECT_CONTEXT_FILE_NAME = "CONTEXT.md"

CLAUDE_AGENT_FILES_PATH = Path(".claude")
CLAUDE_STARTUP_MODEL = "claude-opus-4-6"
CLAUDE_STARTUP_EFFORT = "medium"
CLAUDE_SETTINGS_FILE_NAME = "settings.json"

CONTEXT_FILE_PATH = Path("analysis_context")
NOTES_FILE_PATH = Path("notes")
SKILLS_FILES_PATH = Path("skills")

ANALYSIS_PLAN_FILE_NAME = "analysis_plan.md"
ANALYSIS_OVERVIEW_FILE_NAME = "analysis_overview.md"

DEFAULT_MARIMO_NOTEBOOK_FILE_NAME = "notebook"
DEFAULT_MARIMO_NOTEBOOK_PORT = "8080"


PkgManager = Literal["poetry", "uv", "pip", "conda"]
PACKAGE_MANAGER_INDICATORS = {
    ("poetry.lock",) : "poetry",
    ("uv.lock",): "uv",
    ("environment.yml", "environment.yaml", "conda-lock.yml"): "conda",
    ("requirements.txt", "requirements-dev.txt", "setup.py", "setup.cfg"): "pip"
} 

REQUIRED_DEPENDENCIES = ("marimo>=0.23.15",)

MARIMO_NOTEBOOK_EDIT_BASH = ["run", "marimo", "edit", "--watch"]