import typer
from devinit.cli import app as cli

app = typer.Typer()
app.add_typer(cli)


if __name__ == "__main__":
    app()