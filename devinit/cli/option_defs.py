from pathlib import Path

import typer


GitOption = typer.Option(
    None,
    "--git/--no-git",
    help="Whether to initialize a git repository.",
)

DockerOption = typer.Option(
    None,
    "--docker/--no-docker",
    help="Whether to create a Dockerfile.",
)

EntryOption = typer.Option(
    None,
    "--entry",
    help="The entry point for the application.",
)

PathOption = typer.Option(
    None,
    "--path",
    help="The path where the application will be created.",
)

VersionOption = typer.Option(
    None,
    "--version",
    help="The version of the language/framework to use.",
)

GithubOption = typer.Option(
    None,
    "--github/--no-github",
    help="Whether to create a GitHub repository.",
)

PublicOption = typer.Option(
    None,
    "--public/--private",
    help="Whether the GitHub repository should be public or private.",
)

LicenseOption = typer.Option(
    None,
    "--license",
    help="The license to apply to the project.",
)

ActionsOption = typer.Option(
    None,
    "--actions/--no-actions",
    help="Whether to integrate GitHub Actions.",
)

PMOption = typer.Option(
    None,
    help="Python project manager to use",
)