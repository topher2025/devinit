import typer
from rich import print
from devinit.cli.create import app as create_app
from devinit.cli.config import app as config_app
from devinit.exceptions import DevinitError


app = typer.Typer()
app.add_typer(create_app, name="create")
app.add_typer(config_app, name="config")


if __name__ == "__main__":
    try:
        app()
    except DevinitError as e:
        print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)