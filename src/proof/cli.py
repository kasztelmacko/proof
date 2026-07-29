import typer
from typing import Annotated

from proof.utils import run_command
from proof.commands import create_analysis
from proof.config import ModelsCLI

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False)

@app.command()
def create(
    analysis_name: Annotated[
        str,
        typer.Argument(help="Folder name of the analysis"),
    ]
) -> None:
    run_command(lambda: create_analysis(analysis_name=analysis_name))

@app.command()
def start(
    analysis_name: Annotated[
        str,
        typer.Argument(help="Folder name of the analysis"),
    ],
    model_cli: Annotated[
        ModelsCLI,
        typer.Argument(help="CLI model to use for the analysis")
    ]
) -> None:
    pass


if __name__ == "__main__":
    app()