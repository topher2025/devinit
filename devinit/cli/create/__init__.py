import typer
from pathlib import Path

from devinit.generators.generator import Generator
from devinit.cli.create.python import python

app = typer.Typer()
app.add_typer(python, name="python")

@app.command(
    context_settings={
    "allow_extra_args": True,
    "ignore_unknown_options": True,
    }
)
def local(path: Path, name: str, ctx: typer.Context):
    generator = Generator.from_list(path, name, ctx.args)
    generator.generate()