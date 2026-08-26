import os
import sys
import subprocess
from pathlib import Path

def open_file(file_path):
    fp = os.path.abspath(file_path)
    if sys.platform.startswith("win"):
        os.startfile(fp)  # opens with Windows file association
    elif sys.platform == "darwin":
        subprocess.run(["open", file_path], check=False)
    else:
        subprocess.run(["xdg-open", fp], check=False)

def config_path():
    if sys.platform.startswith("win"):
        appdata = os.getenv("APPDATA")
        if appdata is None:
            return Path.home() / "AppData" / "Roaming" / "devinit" / "config.toml"
        return Path(appdata) / "devinit" / "config.toml"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "devinit" / "config.toml"
    else:
        return Path.home() / ".config" / "devinit" / "config.toml"