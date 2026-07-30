import typer
from typing import Annotated

from proof.utils import run_command
from proof.commands import create_analysis, start_session
from proof.config import ModelsCLI, DEFAULT_NOTEBOOK_FILE_NAME

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
    ] = DEFAULT_NOTEBOOK_FILE_NAME
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
    model_cli: Annotated[
        ModelsCLI,
        typer.Argument(help="CLI model to use for the analysis")
    ],
) -> None:
    run_command(lambda: start_session(analysis_name=analysis_name, notebook_name=notebook_name, model_cli=model_cli))


if __name__ == "__main__":
    app()