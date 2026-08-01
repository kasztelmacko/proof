import typer
from typing import Annotated

from proof.utils import run_command
from proof.commands import create_analysis, start_session
from proof.config import DEFAULT_MARIMO_NOTEBOOK_FILE_NAME, DEFAULT_MARIMO_NOTEBOOK_PORT

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False)

@app.command()
def create(
    analysis_name: Annotated[
        str,
        typer.Argument(help="Folder name of the analysis"),
    ],
    notebook_name: Annotated[
        str,
        typer.Option(
            "--notebook_name",
            "-n",
            help="name for analysis notebook name"
        )
    ] = DEFAULT_MARIMO_NOTEBOOK_FILE_NAME
) -> None:
    run_command(lambda: create_analysis(analysis_name=analysis_name, notebook_name=notebook_name))

@app.command()
def start(
    analysis_name: Annotated[
        str,
        typer.Argument(help="Folder name of the analysis"),
    ],
    notebook_name: Annotated[
        str,
        typer.Argument(help="name of a notebook to run")
    ],
    notebook_port: Annotated[
        str,
        typer.Option(
            "--port",
            "-p",
            help="port on which to start marimo notebook server"
        )
    ] = DEFAULT_MARIMO_NOTEBOOK_PORT
) -> None:
    run_command(lambda: start_session(analysis_name=analysis_name, notebook_name=notebook_name, notebook_port=notebook_port))


if __name__ == "__main__":
    app()