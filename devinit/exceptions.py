"""
Custom exceptions used throughout devinit.

These exceptions are intended to provide clearer, more descriptive errors than
Python's built-in exceptions when something goes wrong internally.
"""


class DevinitError(Exception):
    """Base class for all devinit exceptions."""

    pass


class ManifestError(DevinitError):
    """Base class for all manifest-related exceptions."""

    pass


class ManifestAttributeError(ManifestError, AttributeError):
    """
    Raised when code attempts to access an attribute that does not exist on a
    Manifest object.
    """

    def __init__(self, attribute: str):
        self.attribute = attribute
        super().__init__(f"Manifest has no attribute '{attribute}'.")