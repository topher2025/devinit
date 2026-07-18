from pathlib import Path
import tomlkit

from devinit.exceptions import ManifestAttributeError
from devinit.config.loaders import load_manifest


class ConfigNode:
    def __init__(self, data: dict) -> None:
        for key, value in data.items():
            if isinstance(value, dict):
                value = ConfigNode(value)

            elif isinstance(value, list):
                value = [
                    ConfigNode(item) if isinstance(item, dict) else item
                    for item in value
                ]

            setattr(self, key, value)
        

    def __repr__(self):
        return repr(self.__dict__)
    

    @staticmethod
    def _convert(value):
        if isinstance(value, ConfigNode):
            return {
                key: ConfigNode._convert(val)
                for key, val in value.__dict__.items()
            }

        if isinstance(value, list):
            return [ConfigNode._convert(item) for item in value]

        return value




class Manifest(ConfigNode):
    def __init__(self, path: Path) -> None:

        self.data = load_manifest(path)
        self.full = load_manifest(path, flatten=False)

        super().__init__(self.data)

    def __getattr__(self, name):
        raise ManifestAttributeError(name)
    
