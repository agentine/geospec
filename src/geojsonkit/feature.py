"""Feature and FeatureCollection types."""

from __future__ import annotations

from typing import Any

from .base import GeoJSON


class Feature(GeoJSON):
    """A GeoJSON Feature wrapping a geometry and properties dict."""

    def __init__(
        self,
        id: str | int | None = None,  # noqa: A002
        geometry: dict[str, Any] | None = None,
        properties: dict[str, Any] | None = None,
        **extra: Any,
    ) -> None:
        super().__init__(
            geometry=geometry,
            properties=properties if properties is not None else {},
            **extra,
        )
        if id is not None:
            self["id"] = id


class FeatureCollection(GeoJSON):
    """A GeoJSON FeatureCollection holding a list of Features."""

    def __init__(
        self,
        features: list[Any] | None = None,
        **extra: Any,
    ) -> None:
        super().__init__(
            features=features if features is not None else [],
            **extra,
        )
