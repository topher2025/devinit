from pathlib import Path

import typer


GitOption = typer.Option(
    None,
    "--git/--no-git",
)

DockerOption = typer.Option(
    None,
    "--docker/--no-docker",
)

EntryOption = typer.Option(
    None,
    "--entry",
)

PathOption = typer.Option(
    None,
    "--path",
)

VersionOption = typer.Option(
    None,
    "--version",
)

GithubOption = typer.Option(
    None,
    "--github/--no-github",
)

PublicOption = typer.Option(
    None,
    "--public/--private",
)

LicenseOption = typer.Option(
    None,
    "--license",
)