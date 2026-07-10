import tomlkit

from devinit.config.config import Config

class Prefs:
    @classmethod
    def _save(cls, path, doc) -> None:
        path.write_text(
            tomlkit.dumps(doc),
            encoding="utf-8",
        )

    @classmethod
    def set_pref(cls, key:str, value):
        path = Config.ensure_config()
        doc = Config.load_prefs()

        current = doc
        parts = key.split(".")

        for part in parts[:-1]:
            if part not in current:
                current[part] = tomlkit.table()
            current = current[part]

        old = cls.get_pref(key)
        current[parts[-1]] = value

        cls._save(path, doc)
        return old        

    @classmethod
    def get_pref(cls, key):
        prefs = Config.load_prefs().unwrap()

        for candidate in cls._lookup_keys(key):
            value = cls._get(prefs, candidate)
            if value is not None:
                return (value, "U")

        defaults = Config.load_defaults().unwrap()

        for candidate in cls._lookup_keys(key):
            value = cls._get(defaults, candidate)
            if value is not None:
                return (value, "D")

        return (None, None)


    @staticmethod
    def _lookup_keys(key):
        parts = key.split(".")
        leaf = parts[-1]
        scopes = parts[:-1]

        keys = []

        while scopes:
            keys.append(".".join(scopes + [leaf]))
            scopes.pop()

        keys.append(f"defaults.{leaf}")

        return keys    
    
    @staticmethod
    def _get(doc, key):
        current = doc

        for part in key.split("."):
            if part not in current:
                return None
            current = current[part]

        return current