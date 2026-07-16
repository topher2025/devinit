from pathlib import Path
from importlib.resources import files
import tomlkit
from tomlkit import TOMLDocument



USER_CONFIG = Path.home() / ".config" / "devinit" / "config.toml"



def _load_toml_document(path: Path) -> TOMLDocument:
    with path.open("r", encoding="utf-8") as file:
        return tomlkit.load(file)


def _load_toml_dict(path: Path) -> dict:
    return _load_toml_document(path).unwrap()


def _defaults_resource():
    return files("devinit.config").joinpath("defaults.config")



def load_manifest(path: Path) -> dict:
    return _load_toml_dict(path)


def load_manifest_document(path: Path) -> TOMLDocument:
    return _load_toml_document(path)


def load_config() -> dict:
    if not USER_CONFIG.exists():
        return {}
    return _load_toml_dict(USER_CONFIG)


def load_config_document() -> TOMLDocument:
    if not USER_CONFIG.exists():
        return tomlkit.document()
    return _load_toml_document(USER_CONFIG)


def load_defaults_config() -> dict:
    resource = _defaults_resource()
    with resource.open("r", encoding="utf-8") as file:
        return tomlkit.load(file).unwrap()


def load_defaults_config_document() -> TOMLDocument:
    resource = _defaults_resource()
    with resource.open("r", encoding="utf-8") as file:
        return tomlkit.load(file)