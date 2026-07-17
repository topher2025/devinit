"""
Custom exceptions used throughout devinit.

These exceptions are intended to provide clearer, more descriptive errors than
Python's built-in exceptions when something goes wrong internally.
"""


class DevinitError(Exception): pass

class ManifestError(DevinitError): pass
class ConfigError(DevinitError): pass

class ManifestAttributeError(ManifestError, AttributeError):
    def __init__(self, attribute: str):
        self.attribute = attribute
        super().__init__(f"Manifest has no attribute '{attribute}'.")

class ConfigLoaderKeyError(ConfigError, KeyError):
    def __init__(self, key: str):
        self.key = key
        super().__init__(f"Config file has no key '{key}'.")

class ConfigLoaderDependencyError(ConfigError):
    def __init__(self, *dependency_names: str):
        self.dependency_names = dependency_names
        if len(dependency_names) == 1:
            msg = f"Dependency '{dependency_names[0]}' must be provided together with the others."
        else:
            msg = (
                "Dependencies must be provided together (either all truthy or all falsy). "
                f"Got: {', '.join(dependency_names)}"
            )
        super().__init__(msg)