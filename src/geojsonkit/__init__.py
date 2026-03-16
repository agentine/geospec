"""geojsonkit — GeoJSON for Python (RFC 7946)."""

from __future__ import annotations

from .base import GeoJSON
from .codec import dump, dumps, load, loads
from .feature import Feature, FeatureCollection
from .geometry import (
    Geometry,
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from .utils import coords, map_coords, map_geometries, map_tuples, merge

__all__ = [
    "GeoJSON",
    "Geometry",
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
    "GeometryCollection",
    "Feature",
    "FeatureCollection",
    "dump",
    "dumps",
    "load",
    "loads",
    "coords",
    "map_coords",
    "map_tuples",
    "map_geometries",
    "merge",
]
