import typer
from devinit.cli.create.app import app as create_app

app = typer.Typer()
app.add_typer(create_app, name="create")


if __name__ == "__main__":
    app()