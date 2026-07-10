import typer
from devinit.cli.create import app as create_app
from devinit.cli.config import app as config_app


app = typer.Typer()
app.add_typer(create_app, name="create")
app.add_typer(config_app, name="config")


if __name__ == "__main__":
    app()