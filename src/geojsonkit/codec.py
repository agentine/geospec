"""GeoJSON JSON serialization and deserialization."""

from __future__ import annotations

import json
from typing import IO, Any

from .base import GeoJSON
from .feature import Feature, FeatureCollection
from .geometry import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)

_TYPE_MAP: dict[str, type[GeoJSON]] = {
    "Point": Point,
    "MultiPoint": MultiPoint,
    "LineString": LineString,
    "MultiLineString": MultiLineString,
    "Polygon": Polygon,
    "MultiPolygon": MultiPolygon,
    "GeometryCollection": GeometryCollection,
    "Feature": Feature,
    "FeatureCollection": FeatureCollection,
}


def _object_hook(d: dict[str, Any]) -> Any:
    """Reconstruct GeoJSON objects from parsed dicts."""
    typ = d.get("type")
    if isinstance(typ, str) and typ in _TYPE_MAP:
        cls = _TYPE_MAP[typ]
        obj: GeoJSON = dict.__new__(cls)
        dict.__init__(obj, d)
        return obj
    return d


class GeoJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles objects with __geo_interface__."""

    def default(self, o: Any) -> Any:
        if hasattr(o, "__geo_interface__"):
            return o.__geo_interface__
        return super().default(o)


def dumps(obj: Any, sort_keys: bool = False, **kwargs: Any) -> str:
    """Serialize a GeoJSON object to a JSON string."""
    return json.dumps(obj, sort_keys=sort_keys, cls=GeoJSONEncoder, **kwargs)


def loads(s: str | bytes, **kwargs: Any) -> Any:
    """Deserialize a JSON string to GeoJSON objects."""
    return json.loads(s, object_hook=_object_hook, **kwargs)


def dump(obj: Any, fp: IO[str], sort_keys: bool = False, **kwargs: Any) -> None:
    """Serialize a GeoJSON object to a file."""
    json.dump(obj, fp, sort_keys=sort_keys, cls=GeoJSONEncoder, **kwargs)


def load(fp: IO[str], **kwargs: Any) -> Any:
    """Deserialize a file to GeoJSON objects."""
    return json.load(fp, object_hook=_object_hook, **kwargs)
