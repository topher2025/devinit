import subprocess
import shutil


class Git:
    def __init__(self, cwd):
        self.git = shutil.which("git")
        self.cwd = cwd
        if not self.git:
            return None
        else:
            try:
                subprocess.run([self.git, "--version"], check=True, stdout=subprocess.PIPE, text=True, cwd=self.cwd)
                return None
            except Exception as e:
                return None
    
    def init(self):
        if not self.git: return False
        try:
            subprocess.run(
                [self.git, "init"],
                check=True, cwd=self.cwd)
            return True
        except Exception: return False
    
    def add(self, *args: str):
        if not self.git: return False
        try:
            subprocess.run(
                [self.git, "add", *args],
                check=True, cwd=self.cwd)
            return True
        except Exception: return False

    def commit(self, message: str):
        if not self.git: return False
        try:
            subprocess.run(
                [self.git, "commit", "-m", message],
                check=True, cwd=self.cwd)
            return True
        except Exception: return False