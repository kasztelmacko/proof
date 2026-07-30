from proof.utils import (
    get_project_and_analysis_root,
    detect_pkg_manager
)
from proof.actions import (
    AnalysisContext,
    SessionContext,
    MakeDirectories,
    MakeFiles,
    InstallDependencies,
    WriteConfig,
    RunBashCommands
)
from proof.config import DEFAULT_NOTEBOOK_FILE_NAME, ModelsCLI

def create_analysis(analysis_name: str, notebook_name: str = DEFAULT_NOTEBOOK_FILE_NAME) -> None:
    project_root, analysis_root = get_project_and_analysis_root(analysis_name=analysis_name)
    pkg_manager = detect_pkg_manager(project_root=project_root)

    analysis_context = AnalysisContext(
        analysis_name=analysis_name,
        project_root=project_root,
        analysis_root=analysis_root,
        pkg_manager=pkg_manager
    )

    MakeDirectories(analysis_context).create()
    MakeFiles(analysis_context).create(notebook_name=notebook_name)
    InstallDependencies(analysis_context).create()
    WriteConfig(analysis_context).create()


def start_session(analysis_name: str, notebook_name: str, model_cli: ModelsCLI) -> None:
    project_root, analysis_root = get_project_and_analysis_root(analysis_name=analysis_name)
    pkg_manager = detect_pkg_manager(project_root=project_root)

    analysis_context = AnalysisContext(
        analysis_name=analysis_name,
        project_root=project_root,
        analysis_root=analysis_root,
        pkg_manager=pkg_manager,
    )

    session_context = SessionContext(
        model_cli=model_cli,
        notebook_name=notebook_name
    )

    RunBashCommands(analysis_context, session_context).start()