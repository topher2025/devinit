import typer
from importlib.metadata import version as package_version
from pathlib import Path
from typing import Annotated

from devinit.cli.option_defs import (
    GitOption,
    DockerOption,
    EntryOption,
    PathOption,
    VersionOption,
    GithubOption,
    PublicOption,
    LicenseOption,
)
from devinit.models import option_classes
from devinit.config.config import Config
from devinit.generators.python import FlaskGenerator
from devinit.cli.create.update import updater

python = typer.Typer()
@python.command()
def flask(
    name: str,
    git: bool | None = GitOption,
    docker: bool | None = DockerOption,
    entry: str | None = EntryOption,
    path: Path | None = PathOption,
    version: str | None = VersionOption,
    github: bool | None = GithubOption,
    public: bool | None = PublicOption,
    blueprints: bool | None = typer.Option(
        None,
        "--blueprints/--no-blueprints",
    ),
    license: str | None = LicenseOption,
):
    context = Config.resolve(locals(), "python", "flask")

    updater(
        generator=FlaskGenerator,
        context=context,
        name=name,
        output=context["path"]
    )

