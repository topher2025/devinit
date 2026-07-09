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
    github: str | None = GithubOption,
    public: bool | None = PublicOption,
    blueprints: bool | None = typer.Option(
        None,
        "--blueprints/--no-blueprints",
    ),
):
    context = Config.resolve(locals(), "python", "flask")
    output_dir = context["path"] / name
    defaults = Config.load_defaults().unwrap()
    context["project"] = name
    context["path"] = output_dir
    context["devinit_version"] = package_version("devinit")
    context["license"] = defaults["defaults"]["license"]
    context["license_type"] = context["license"]
    generator = FlaskGenerator()
    updater(
        generator=generator,
        context=context,
        name=name,
        output=output_dir
    )

