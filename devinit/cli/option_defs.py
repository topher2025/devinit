from pathlib import Path
from typing import Annotated

import typer


GitOption = Annotated[
    bool | None,
    typer.Option(None, "--git/--no-git"),
]

DockerOption = Annotated[
    bool | None,
    typer.Option(None, "--docker/--no-docker"),
]

EntryOption = Annotated[
    str | None,
    typer.Option(None, "--entry"),
]

PathOption = Annotated[
    Path | None,
    typer.Option(None, "--path"),
]

VersionOption = Annotated[
    str | None,
    typer.Option(None, "--version"),
]