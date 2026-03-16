"""RFC 7946 validation logic for GeoJSON objects."""

from __future__ import annotations

from typing import Any

_VALID_TYPES = frozenset({
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
    "GeometryCollection",
    "Feature",
    "FeatureCollection",
})

_GEOMETRY_TYPES = frozenset({
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
})


def _validate_position(position: Any, errs: list[str]) -> None:
    if not isinstance(position, (list, tuple)):
        errs.append(
            f"Position must be a list or tuple, got {type(position).__name__}"
        )
        return
    n = len(position)
    if n < 2 or n > 3:
        errs.append(f"Position must have 2 or 3 values, got {n}")
        return
    for v in position:
        if not isinstance(v, (int, float)):
            errs.append(
                f"Coordinate values must be numbers, got {type(v).__name__}"
            )
            return
    lon: float = position[0]
    lat: float = position[1]
    if lon < -180 or lon > 180:
        errs.append(f"Longitude {lon} out of range [-180, 180]")
    if lat < -90 or lat > 90:
        errs.append(f"Latitude {lat} out of range [-90, 90]")


def _validate_linestring_coords(coords: Any, errs: list[str]) -> None:
    if not isinstance(coords, (list, tuple)):
        errs.append("LineString coordinates must be an array")
        return
    if len(coords) < 2:
        errs.append(
            f"LineString must have at least 2 positions, got {len(coords)}"
        )
        return
    for pos in coords:
        _validate_position(pos, errs)


def _validate_linear_ring(ring: Any, ring_idx: int, errs: list[str]) -> None:
    if not isinstance(ring, (list, tuple)):
        errs.append(f"Ring {ring_idx} must be an array")
        return
    if len(ring) < 4:
        errs.append(
            f"Ring {ring_idx} must have at least 4 positions, got {len(ring)}"
        )
        return
    if list(ring[0]) != list(ring[-1]):
        errs.append(f"Ring {ring_idx} is not closed (first != last position)")
    for pos in ring:
        _validate_position(pos, errs)


def _validate_polygon_coords(coords: Any, errs: list[str]) -> None:
    if not isinstance(coords, (list, tuple)):
        errs.append("Polygon coordinates must be an array of linear rings")
        return
    if len(coords) < 1:
        errs.append("Polygon must have at least 1 linear ring")
        return
    for i, ring in enumerate(coords):
        _validate_linear_ring(ring, i, errs)


def errors(obj: dict[str, Any]) -> list[str]:
    """Return a list of RFC 7946 validation errors for a GeoJSON object."""
    errs: list[str] = []
    typ = obj.get("type")

    if typ is None:
        errs.append("'type' member is required")
        return errs
    if typ not in _VALID_TYPES:
        errs.append(f"'{typ}' is not a valid GeoJSON type")
        return errs

    if typ in _GEOMETRY_TYPES:
        if "coordinates" not in obj:
            errs.append(f"'{typ}' requires a 'coordinates' member")
            return errs
        coords = obj["coordinates"]
        if coords is None:
            return errs

        if typ == "Point":
            _validate_position(coords, errs)
        elif typ == "MultiPoint":
            if not isinstance(coords, (list, tuple)):
                errs.append("MultiPoint coordinates must be an array")
            else:
                for pos in coords:
                    _validate_position(pos, errs)
        elif typ == "LineString":
            _validate_linestring_coords(coords, errs)
        elif typ == "MultiLineString":
            if not isinstance(coords, (list, tuple)):
                errs.append("MultiLineString coordinates must be an array")
            else:
                for line in coords:
                    _validate_linestring_coords(line, errs)
        elif typ == "Polygon":
            _validate_polygon_coords(coords, errs)
        elif typ == "MultiPolygon":
            if not isinstance(coords, (list, tuple)):
                errs.append("MultiPolygon coordinates must be an array")
            else:
                for poly in coords:
                    _validate_polygon_coords(poly, errs)

    elif typ == "GeometryCollection":
        if "geometries" not in obj:
            errs.append("'GeometryCollection' requires a 'geometries' member")
        else:
            geoms = obj["geometries"]
            if not isinstance(geoms, (list, tuple)):
                errs.append("'geometries' must be an array")
            else:
                for i, g in enumerate(geoms):
                    if not isinstance(g, dict):
                        errs.append(f"geometries[{i}]: must be an object")
                        continue
                    for err in errors(g):
                        errs.append(f"geometries[{i}]: {err}")

    elif typ == "Feature":
        if "geometry" not in obj:
            errs.append("'Feature' requires a 'geometry' member")
        else:
            geom = obj["geometry"]
            if geom is not None:
                if not isinstance(geom, dict):
                    errs.append("'geometry' must be an object or null")
                else:
                    for err in errors(geom):
                        errs.append(f"geometry: {err}")
        if "properties" not in obj:
            errs.append("'Feature' requires a 'properties' member")

    elif typ == "FeatureCollection":
        if "features" not in obj:
            errs.append("'FeatureCollection' requires a 'features' member")
        else:
            features = obj["features"]
            if not isinstance(features, (list, tuple)):
                errs.append("'features' must be an array")
            else:
                for i, f in enumerate(features):
                    if not isinstance(f, dict):
                        errs.append(f"features[{i}]: must be an object")
                        continue
                    for err in errors(f):
                        errs.append(f"features[{i}]: {err}")

    return errs


def is_valid(obj: dict[str, Any]) -> bool:
    """Return True if the GeoJSON object has no validation errors."""
    return len(errors(obj)) == 0
