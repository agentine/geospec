"""Tests for JSON codec (dumps/loads/dump/load)."""

import io

from geojsonkit import (
    Feature,
    FeatureCollection,
    GeometryCollection,
    LineString,
    Point,
    Polygon,
    dump,
    dumps,
    load,
    loads,
)


class TestDumps:
    def test_point(self) -> None:
        p = Point([0, 0])
        s = dumps(p)
        assert '"type": "Point"' in s or '"type":"Point"' in s

    def test_sort_keys(self) -> None:
        p = Point([0, 0])
        s = dumps(p, sort_keys=True)
        # coordinates comes before type alphabetically
        assert s.index("coordinates") < s.index("type")

    def test_feature(self) -> None:
        f = Feature(geometry=Point([1, 2]), properties={"name": "test"})
        s = dumps(f)
        assert "Feature" in s
        assert "test" in s

    def test_feature_collection(self) -> None:
        fc = FeatureCollection(features=[Feature(geometry=Point([0, 0]))])
        s = dumps(fc)
        assert "FeatureCollection" in s


class TestLoads:
    def test_point(self) -> None:
        s = '{"type": "Point", "coordinates": [1.5, 2.5]}'
        obj = loads(s)
        assert isinstance(obj, Point)
        assert obj["coordinates"] == [1.5, 2.5]

    def test_linestring(self) -> None:
        s = '{"type": "LineString", "coordinates": [[0, 0], [1, 1]]}'
        obj = loads(s)
        assert isinstance(obj, LineString)

    def test_polygon(self) -> None:
        s = '{"type": "Polygon", "coordinates": [[[0,0],[1,0],[1,1],[0,0]]]}'
        obj = loads(s)
        assert isinstance(obj, Polygon)

    def test_feature(self) -> None:
        s = '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [0, 0]}, "properties": {}}'
        obj = loads(s)
        assert isinstance(obj, Feature)
        assert isinstance(obj["geometry"], Point)

    def test_feature_collection(self) -> None:
        s = '{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": {"type": "Point", "coordinates": [0, 0]}, "properties": {}}]}'
        obj = loads(s)
        assert isinstance(obj, FeatureCollection)
        assert isinstance(obj["features"][0], Feature)

    def test_geometry_collection(self) -> None:
        s = '{"type": "GeometryCollection", "geometries": [{"type": "Point", "coordinates": [0, 0]}]}'
        obj = loads(s)
        assert isinstance(obj, GeometryCollection)
        assert isinstance(obj["geometries"][0], Point)

    def test_unknown_type(self) -> None:
        s = '{"type": "Unknown", "data": 1}'
        obj = loads(s)
        assert isinstance(obj, dict)
        assert not isinstance(obj, Point)

    def test_no_type(self) -> None:
        s = '{"foo": "bar"}'
        obj = loads(s)
        assert isinstance(obj, dict)
        assert obj["foo"] == "bar"


class TestRoundTrip:
    def test_point(self) -> None:
        p = Point([1.5, 2.5])
        result = loads(dumps(p))
        assert isinstance(result, Point)
        assert result["coordinates"] == [1.5, 2.5]

    def test_feature(self) -> None:
        f = Feature(id="x", geometry=Point([0, 0]), properties={"a": 1})
        result = loads(dumps(f))
        assert isinstance(result, Feature)
        assert result["id"] == "x"
        assert result["properties"]["a"] == 1

    def test_feature_collection(self) -> None:
        fc = FeatureCollection(features=[
            Feature(geometry=Point([0, 0])),
            Feature(geometry=Point([1, 1])),
        ])
        result = loads(dumps(fc))
        assert isinstance(result, FeatureCollection)
        assert len(result["features"]) == 2


class TestDumpLoad:
    def test_file_round_trip(self) -> None:
        p = Point([1, 2])
        fp = io.StringIO()
        dump(p, fp)
        fp.seek(0)
        result = load(fp)
        assert isinstance(result, Point)
        assert result["coordinates"] == [1, 2]
