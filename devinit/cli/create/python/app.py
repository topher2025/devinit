import typer

from typing import Annotated

from devinit.cli.option_defs import (
    GitOption,
    DockerOption,
    EntryOption,
    PathOption,
    VersionOption
)
from devinit.models import option_classes
from devinit.config.resolver import resolve

app = typer.Typer()

@app.command()
def flask(
    name: str,
    git: GitOption,
    docker: DockerOption,
    entry: EntryOption,
    path: PathOption,
    version: VersionOption
):
    context = resolve()