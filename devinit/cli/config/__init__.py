import typer
from rich import print

from devinit.config.prefs import Prefs

app = typer.Typer()

@app.command("set")
def set_config(
    key: str,
    value: str,
):
    old = Prefs.set_pref(key, value)
    if old[1] == "U":
        print(f"[cyan]{key}[/cyan]: [red]{old[0]}[/red] → [green]{value}[/green]")
    elif old[1] == "D":
        print(f"[cyan]{key}[/cyan]: [red]{old[0]}[/red] → [green]{value}[/green] (came from defaults)")