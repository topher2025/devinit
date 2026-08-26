import typer
from rich import print
from rich.pretty import Pretty
import re



from devinit.config.prefs import Prefs
from devinit.config.nxt_config import Config

app = typer.Typer()
config = Config()





@app.command("set")
def set_config(key: str, value: str):
    config.set_value(re.split(r"[./]+", key), value)
    

@app.command("reset")
def reset_config():
    try: config.reset()
    except Exception as e: print(e)

@app.command("unset")
def unset_config(key: str):
    config.unset_value(re.split(r"[./]+", key))


@app.command("get")
def get_config(key: str):
    value = config.get_value(re.split(r"[./]+", key))
    print(Pretty({key: value}))

@app.command("list")
def list_config(key: str):
    print("Doesn't Work"); return
    value = config.list(re.split(r"[./]+", key))
    print(Pretty(value))


@app.command("edit")
def edit_config():
    try: config.edit()
    except Exception as e: print(e)
