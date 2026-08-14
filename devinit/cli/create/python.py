import typer
from importlib.metadata import version as package_version
from pathlib import Path
from typing import Annotated, Literal

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



from devinit.generators.generator import Generator

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


@python.commmand()
def fastapi(
    name: str,
    path: Path | None = PathOption,
    actions: bool | None = typer.Option(
        None,
        "--actions/--no-actions",
        help="Whether to integrate GitHub Actions.",
    ),
    async: bool | None = typer.Option(
        None,
        "--async/--no-async",
        help="Will the web app use async endpoints.",
    ),
    auth: Literal["jwt", "oauth"] | None = typer.Option(
        None,
        help="Authentication method to be used.",
    ),
    database: Literal["mysql", "postgresql", "sqlite"] | None = typer.Option(
        None,
        help="SQL library to use.",
    ),
    docker: bool | None = DockerOption,
    git: bool | None = GitOption,
    github: bool | None = GithubOption,
    migrations: bool | None = typer.Option(
        None,
        "--migrations/--no-migrations",
        help="Whether to enable database migrations.",
    ),
    orm: Literal["sqlalchemy", "sqlmodel"] | None = typer.Option(
        None,
        help="Python library to use for DB ORM",
    ),
    pm: Literal["pip", "uv"] | None = typer.Option(
        None,
        help="Python project manager to use",
    ),
):
    generator = Generator.from_list(path, name, locals())
    generator.generate()

