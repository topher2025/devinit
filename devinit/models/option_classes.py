from dataclasses import dataclass
from pathlib import Path


@dataclass
class CreateOptions:
    git: bool
    docker: bool
    entry: str
    path: Path
    version: str