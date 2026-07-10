import tomlkit
from importlib.resources import files
from importlib.metadata import version
from pathlib import Path
from datetime import datetime



class Config:
    @classmethod
    def resolve(cls, inputs: dict, lang: str, framework: str = "") -> dict:
        defaults = cls.load_defaults().unwrap()
        preferences = cls.load_prefs().unwrap()
        resolved = {}
        for k, v in inputs.items():
            if v is not None:
                resolved[k] = v
                continue
            if lang in preferences:
                if framework != "" and framework in preferences[lang] and k in preferences[lang][framework]:
                    resolved[k] = preferences[lang][framework][k]
                    continue
                if k in preferences[lang]:
                    resolved[k] = preferences[lang][k]
                    continue
            if "defaults" in preferences and k in preferences["defaults"]:
                resolved[k] = preferences["defaults"][k]
                continue
            if framework != "" and k in defaults[lang][framework]:
                resolved[k] = defaults[lang][framework][k]
                continue
            if k in defaults[lang]:
                resolved[k] = defaults[lang][k]
                continue
            resolved[k] = defaults["defaults"][k]


        resolved["path"] = Path(resolved["path"]) / resolved["name"]
        resolved["devinit_version"] = version("devinit")
        resolved["year"] = datetime.now().year
        if "name" in preferences:
            resolved["name"] = preferences["name"]
        else:
            print(defaults)
            resolved["name"] = defaults["name"]


        return resolved
    
    @classmethod
    def load_defaults(cls) -> tomlkit.TOMLDocument:
        default_file = files("devinit.config").joinpath("defaults.toml")
        return tomlkit.parse(default_file.read_text(encoding="utf-8"))

    @classmethod
    def load_prefs(cls) -> tomlkit.TOMLDocument:
        path = cls._pref_path()

        if not path.exists():
            return tomlkit.document()

        return tomlkit.parse(path.read_text(encoding="utf-8"))
    

    @staticmethod
    def _pref_path():
        return Path.home() / ".config" / "devinit" / "config.toml"
    


    @classmethod
    def ensure_config(cls) -> Path:
        path = cls._pref_path()

        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            path.write_text(
                tomlkit.dumps(tomlkit.document()),
                encoding="utf-8",
            )

        return path
    
