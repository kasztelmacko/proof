from proof.utils import (
    get_project_and_analysis_root,
    detect_pkg_manager
)
from proof.actions import (
    ProjectContext,
    AnalysisContext,
    SessionContext,
    MakeDirectories,
    MakeFiles,
    CopyFiles,
    InstallDependencies,
    WriteToFiles,
    RunBashCommands,
    SymlinkFiles,
    PrintToConsole
)
from proof.config import DEFAULT_MARIMO_NOTEBOOK_FILE_NAME, DEFAULT_MARIMO_NOTEBOOK_PORT

def init_proof() -> None:
    project_root, _ = get_project_and_analysis_root()
    pkg_manager = detect_pkg_manager(project_root=project_root)

    project_context = ProjectContext(
        project_root=project_root,
        pkg_manager=pkg_manager
    )

    RunBashCommands(project_context).init()
    MakeDirectories(project_context).init()
    MakeFiles(project_context).init()
    InstallDependencies(project_context).init()
    WriteToFiles(project_context).init()
    PrintToConsole(project_context).init()

def create_analysis(analysis_name: str, notebook_name: str = DEFAULT_MARIMO_NOTEBOOK_FILE_NAME) -> None:
    project_root, analysis_root = get_project_and_analysis_root(analysis_name=analysis_name)
    pkg_manager = detect_pkg_manager(project_root=project_root)

    project_context = ProjectContext(
        project_root=project_root,
        pkg_manager=pkg_manager
    )

    analysis_context = AnalysisContext(
        analysis_name=analysis_name,
        analysis_root=analysis_root,
    )

    MakeDirectories(project_context, analysis_context).create()
    MakeFiles(project_context, analysis_context).create(notebook_name=notebook_name)
    CopyFiles(project_context, analysis_context).create()
    SymlinkFiles(project_context, analysis_context).create()


def start_session(analysis_name: str, notebook_name: str, notebook_port: str = DEFAULT_MARIMO_NOTEBOOK_PORT) -> None:
    project_root, analysis_root = get_project_and_analysis_root(analysis_name=analysis_name)
    pkg_manager = detect_pkg_manager(project_root=project_root)

    project_context = ProjectContext(
        project_root=project_root,
        pkg_manager=pkg_manager
    )

    analysis_context = AnalysisContext(
        analysis_name=analysis_name,
        analysis_root=analysis_root,
    )

    session_context = SessionContext(
        notebook_name=notebook_name,
        notebook_port=notebook_port
    )

    RunBashCommands(project_context, analysis_context, session_context).start()


def add_notebook(analysis_name: str, notebook_name: str) -> None:
    project_root, analysis_root = get_project_and_analysis_root(analysis_name=analysis_name)
    pkg_manager = detect_pkg_manager(project_root=project_root)

    project_context = ProjectContext(
        project_root=project_root,
        pkg_manager=pkg_manager
    )

    analysis_context = AnalysisContext(
        analysis_name=analysis_name,
        analysis_root=analysis_root,
    )

    MakeFiles(project_context, analysis_context).add(notebook_name=notebook_name)


def add_symlink(analysis_name: str, path: str) -> None:
    project_root, analysis_root = get_project_and_analysis_root(analysis_name=analysis_name)
    pkg_manager = detect_pkg_manager(project_root=project_root)

    project_context = ProjectContext(
        project_root=project_root,
        pkg_manager=pkg_manager
    )

    analysis_context = AnalysisContext(
        analysis_name=analysis_name,
        analysis_root=analysis_root,
    )

    SymlinkFiles(project_context, analysis_context).add(path=path)