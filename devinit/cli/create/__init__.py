import typer

from devinit.cli.create.python import python

app = typer.Typer()
app.add_typer(python, name="python")