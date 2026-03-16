"""RFC 7946 geometry types."""

from __future__ import annotations

from typing import Any

from .base import GeoJSON


def _apply_precision(coords: Any, precision: int) -> Any:
    """Recursively round coordinate values to *precision* decimal places."""
    if isinstance(coords, (int, float)):
        return round(coords, precision)
    if isinstance(coords, (list, tuple)):
        return [_apply_precision(c, precision) for c in coords]
    return coords


class Geometry(GeoJSON):
    """Base class for geometry types with coordinates."""

    def __init__(
        self,
        coordinates: Any = None,
        validate: bool = False,
        precision: int = 6,
        **extra: Any,
    ) -> None:
        if coordinates is not None:
            coordinates = _apply_precision(coordinates, precision)
        super().__init__(coordinates=coordinates, **extra)
        if validate and not self.is_valid:
            raise ValueError(
                f"Invalid {self['type']}: {'; '.join(self.errors())}"
            )


class Point(Geometry):
    """A GeoJSON Point geometry."""


class MultiPoint(Geometry):
    """A GeoJSON MultiPoint geometry."""


class LineString(Geometry):
    """A GeoJSON LineString geometry."""


class MultiLineString(Geometry):
    """A GeoJSON MultiLineString geometry."""


class Polygon(Geometry):
    """A GeoJSON Polygon geometry."""


class MultiPolygon(Geometry):
    """A GeoJSON MultiPolygon geometry."""


class GeometryCollection(GeoJSON):
    """A GeoJSON GeometryCollection."""

    def __init__(
        self,
        geometries: list[Any] | None = None,
        **extra: Any,
    ) -> None:
        super().__init__(
            geometries=geometries if geometries is not None else [],
            **extra,
        )
