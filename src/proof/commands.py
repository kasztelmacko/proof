from proof.utils import (
    get_project_and_analysis_root,
    detect_pkg_manager
)
from proof.actions import (
    AnalysisContext,
    MakeDirectories,
    MakeFiles,
    InstallDependencies,
    WriteConfig,
)
from proof.config import DEFAULT_NOTEBOOK_FILE_NAME

def create_analysis(analysis_name: str, notebook_name: str = DEFAULT_NOTEBOOK_FILE_NAME) -> None:
    project_root, analysis_root = get_project_and_analysis_root(analysis_name=analysis_name)
    pkg_manager = detect_pkg_manager(project_root=project_root)

    context = AnalysisContext(
        analysis_name=analysis_name,
        project_root=project_root,
        analysis_root=analysis_root,
        pkg_manager=pkg_manager
    )

    MakeDirectories(context).create()
    MakeFiles(context).create(notebook_name=notebook_name)
    InstallDependencies(context).create()
    WriteConfig(context).create()