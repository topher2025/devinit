import typer
from importlib.resources import as_file, files
from pathlib import Path
from typing import Annotated, Literal

from devinit.cli.option_defs import *
from devinit.config.config import Config
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
    github: bool | None = GithubOption,
    public: bool | None = PublicOption,
    blueprints: bool | None = typer.Option(
        None,
        "--blueprints/--no-blueprints",
        help="Whether to use blueprints as part ofthe project structure.",
    ),
    license: str | None = LicenseOption,
):
    with as_file(files("devinit.templates.python") / "flask") as template_path:
        generator = Generator.from_locals(template_path, name, locals())
        generator.generate()


@python.command()
def fastapi(
    name: str,
    path: Path | None = PathOption,
    actions: bool | None = ActionsOption,
    aasync: bool | None = typer.Option(
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
    pm: Literal["pip", "uv"] | None = PMOption,
):
    with as_file(files("devinit.templates.python") / "fastapi-web") as template_path:
        generator = Generator.from_locals(template_path, name, locals())
        generator.generate()


