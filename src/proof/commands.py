from proof.utils import (
    get_project_and_analysis_root,
    detect_pkg_manager
)
from proof.actions import (
    AnalysisContext,
    SessionContext,
    MakeDirectories,
    MakeFiles,
    CopyFiles,
    InstallDependencies,
    WriteToFiles,
    RunBashCommands
)
from proof.config import DEFAULT_NOTEBOOK_FILE_NAME

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
    CopyFiles(analysis_context).create()
    InstallDependencies(analysis_context).create()
    WriteToFiles(analysis_context).create()


def start_session(analysis_name: str, notebook_name: str) -> None:
    project_root, analysis_root = get_project_and_analysis_root(analysis_name=analysis_name)
    pkg_manager = detect_pkg_manager(project_root=project_root)

    analysis_context = AnalysisContext(
        analysis_name=analysis_name,
        project_root=project_root,
        analysis_root=analysis_root,
        pkg_manager=pkg_manager,
    )

    session_context = SessionContext(
        notebook_name=notebook_name
    )

    RunBashCommands(analysis_context, session_context).start()