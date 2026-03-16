"""Coordinate utility functions."""

from __future__ import annotations

from collections.abc import Callable, Generator
from typing import Any

_COORD_GEOMETRY_TYPES = frozenset({
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
})


def coords(obj: dict[str, Any]) -> Generator[tuple[float, ...], None, None]:
    """Yield coordinate tuples from any GeoJSON object."""
    typ = obj.get("type")
    if typ == "Point":
        c = obj.get("coordinates")
        if c is not None:
            yield tuple(c)
    elif typ in ("MultiPoint", "LineString"):
        for pos in obj.get("coordinates", []):
            yield tuple(pos)
    elif typ in ("MultiLineString", "Polygon"):
        for ring in obj.get("coordinates", []):
            for pos in ring:
                yield tuple(pos)
    elif typ == "MultiPolygon":
        for polygon in obj.get("coordinates", []):
            for ring in polygon:
                for pos in ring:
                    yield tuple(pos)
    elif typ == "GeometryCollection":
        for geom in obj.get("geometries", []):
            yield from coords(geom)
    elif typ == "Feature":
        geom = obj.get("geometry")
        if geom is not None:
            yield from coords(geom)
    elif typ == "FeatureCollection":
        for feature in obj.get("features", []):
            yield from coords(feature)


def _map_values(func: Callable[[float], float], coordinates: Any) -> Any:
    """Recursively apply *func* to each scalar coordinate value."""
    if isinstance(coordinates, (int, float)):
        return func(coordinates)
    if isinstance(coordinates, (list, tuple)):
        return [_map_values(func, c) for c in coordinates]
    return coordinates


def _is_position(value: Any) -> bool:
    return (
        isinstance(value, (list, tuple))
        and len(value) > 0
        and isinstance(value[0], (int, float))
    )


def _map_tuples_recursive(
    func: Callable[[tuple[float, ...]], tuple[float, ...]],
    coordinates: Any,
) -> Any:
    """Recursively apply *func* to each position tuple."""
    if _is_position(coordinates):
        return list(func(tuple(coordinates)))
    if isinstance(coordinates, (list, tuple)):
        return [_map_tuples_recursive(func, c) for c in coordinates]
    return coordinates


def _rebuild(obj: dict[str, Any], **overrides: Any) -> Any:
    """Create a new GeoJSON object of the same type with overrides."""
    from .codec import _TYPE_MAP

    data = dict(obj)
    data.update(overrides)
    typ = data.get("type")
    if isinstance(typ, str) and typ in _TYPE_MAP:
        cls = _TYPE_MAP[typ]
        new_obj: Any = dict.__new__(cls)
        dict.__init__(new_obj, data)
        return new_obj
    return data


def map_coords(
    func: Callable[[float], float],
    obj: dict[str, Any],
) -> Any:
    """Apply *func* to each individual coordinate value and return a new object."""
    typ = obj.get("type")
    if typ in _COORD_GEOMETRY_TYPES:
        new_coords = _map_values(func, obj.get("coordinates"))
        return _rebuild(obj, coordinates=new_coords)
    elif typ == "GeometryCollection":
        new_geoms = [map_coords(func, g) for g in obj.get("geometries", [])]
        return _rebuild(obj, geometries=new_geoms)
    elif typ == "Feature":
        geom = obj.get("geometry")
        new_geom = map_coords(func, geom) if geom is not None else None
        return _rebuild(obj, geometry=new_geom)
    elif typ == "FeatureCollection":
        new_features = [map_coords(func, f) for f in obj.get("features", [])]
        return _rebuild(obj, features=new_features)
    return obj


def map_tuples(
    func: Callable[[tuple[float, ...]], tuple[float, ...]],
    obj: dict[str, Any],
) -> Any:
    """Apply *func* to each coordinate tuple and return a new object."""
    typ = obj.get("type")
    if typ in _COORD_GEOMETRY_TYPES:
        new_coords = _map_tuples_recursive(func, obj.get("coordinates"))
        return _rebuild(obj, coordinates=new_coords)
    elif typ == "GeometryCollection":
        new_geoms = [map_tuples(func, g) for g in obj.get("geometries", [])]
        return _rebuild(obj, geometries=new_geoms)
    elif typ == "Feature":
        geom = obj.get("geometry")
        new_geom = map_tuples(func, geom) if geom is not None else None
        return _rebuild(obj, geometry=new_geom)
    elif typ == "FeatureCollection":
        new_features = [map_tuples(func, f) for f in obj.get("features", [])]
        return _rebuild(obj, features=new_features)
    return obj


def map_geometries(
    func: Callable[[dict[str, Any]], dict[str, Any]],
    obj: dict[str, Any],
) -> Any:
    """Apply *func* to each geometry in *obj* and return a new object."""
    typ = obj.get("type")
    if typ in _COORD_GEOMETRY_TYPES:
        return func(obj)
    elif typ == "GeometryCollection":
        new_geoms = [func(g) for g in obj.get("geometries", [])]
        return _rebuild(obj, geometries=new_geoms)
    elif typ == "Feature":
        geom = obj.get("geometry")
        new_geom = func(geom) if geom is not None else None
        return _rebuild(obj, geometry=new_geom)
    elif typ == "FeatureCollection":
        new_features = [
            map_geometries(func, f) for f in obj.get("features", [])
        ]
        return _rebuild(obj, features=new_features)
    return obj


def merge(*objects: dict[str, Any]) -> Any:
    """Merge GeoJSON objects into a single FeatureCollection."""
    from .feature import Feature, FeatureCollection

    features: list[Any] = []
    for obj in objects:
        typ = obj.get("type")
        if typ == "FeatureCollection":
            features.extend(obj.get("features", []))
        elif typ == "Feature":
            features.append(obj)
        else:
            features.append(Feature(geometry=obj))
    return FeatureCollection(features=features)
