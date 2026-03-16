"""GeoJSON base class — dict subclass with attribute access."""

from __future__ import annotations

from typing import Any


class GeoJSON(dict[str, Any]):
    """Base class for all GeoJSON objects.

    A dict subclass that provides attribute-style access and
    implements the __geo_interface__ protocol.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self["type"] = type(self).__name__

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute {name!r}"
            ) from None

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __delattr__(self, name: str) -> None:
        try:
            del self[name]
        except KeyError:
            raise AttributeError(name) from None

    def __repr__(self) -> str:
        return f"{type(self).__name__}({dict.__repr__(self)})"

    @property
    def __geo_interface__(self) -> dict[str, Any]:
        return dict(self)

    @property
    def is_valid(self) -> bool:
        """Return True if this object has no validation errors."""
        return len(self.errors()) == 0

    def errors(self) -> list[str]:
        """Return a list of validation error strings."""
        from . import validation as _validation

        return _validation.errors(self)
