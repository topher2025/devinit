import typer

from devinit.cli.create.python.app import app as python_app

app = typer.Typer()
app.add_typer(python_app, name="python")