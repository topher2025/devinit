import os
import sys
import subprocess

def open_file(file_path):
    fp = os.path.abspath(file_path)
    if sys.platform.startswith("win"):
        os.startfile(fp)  # opens with Windows file association
    elif sys.platform == "darwin":
        subprocess.run(["open", file_path], check=False)
    else:
        subprocess.run(["xdg-open", fp], check=False)