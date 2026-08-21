import typer
from devinit.config.loaders import load_config


def require_name():
    if not load_config().get("fullname") or load_config()["fullname"] == "John Doe":
        raise typer.BadParameter(
            "No name configured. Set one with `devinit config set fullname <full name>`."
        )
