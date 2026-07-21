from pathlib import Path
from importlib.resources import files
from importlib.resources.abc import Traversable
import tomlkit
from tomlkit import TOMLDocument
from devinit.exceptions import *


USER_CONFIG = Path.home() / ".config" / "devinit" / "config.toml"
PathLike = Path | Traversable



def _load_toml_document(path: PathLike) -> TOMLDocument:
    with path.open("r", encoding="utf-8") as file:
        return tomlkit.load(file)


def _load_toml_dict(path: PathLike) -> dict:
    return _load_toml_document(path).unwrap()


def _defaults_resource() -> Traversable:
    return files("devinit.config").joinpath("defaults.toml")


def _flatten(d: dict, r: bool = True) -> dict:
    flat = {}
    for key, value in d.items():
        if isinstance(value, dict):
            if r:
                flat.update(_flatten(value))
        else:
            flat[key] = value
    return flat


def _load_framework(lang: str, framework: str, config: dict) -> dict:
    load = {}
    try:
        load = dict(config["defaults"])
        load.update(_flatten(config[lang], r=False))
        load.update(_flatten(config[lang][framework]))
    except KeyError:
        pass
    
    return load



def load_manifest(path: Path, flatten: bool = True) -> dict:
    if flatten:
        return _flatten(_load_toml_dict(path))
    return _load_toml_dict(path)


def load_manifest_document(path: Path) -> TOMLDocument:
    return _load_toml_document(path)


def load_config(framework: str | None = None, lang: str | None = None) -> dict:
    if bool(framework) ^ bool(lang):
        raise ConfigLoaderDependencyError("lang", "framework")
    
    config = _load_toml_dict(USER_CONFIG)

    if framework and lang:
        config = _load_framework(lang, framework, config)
        
    return config


def load_config_document() -> TOMLDocument:
    if not USER_CONFIG.exists():
        return tomlkit.document()
    return _load_toml_document(USER_CONFIG)


def load_defaults_config(framework: str | None = None, lang: str | None = None) -> dict:
    resource = _defaults_resource()
    config = _load_toml_dict(resource)

    if framework and lang:
        config = _load_framework(lang, framework, config)
        
    return config


def load_defaults_config_document() -> TOMLDocument:
    resource = _defaults_resource()
    with resource.open("r", encoding="utf-8") as file:
        return tomlkit.load(file)