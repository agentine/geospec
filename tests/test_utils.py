"""Tests for utility functions."""

from geojsonkit import (
    Feature,
    FeatureCollection,
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
    coords,
    map_coords,
    map_geometries,
    map_tuples,
    merge,
)


class TestCoords:
    def test_point(self) -> None:
        result = list(coords(Point([1, 2])))
        assert result == [(1, 2)]

    def test_point_3d(self) -> None:
        result = list(coords(Point([1, 2, 3])))
        assert result == [(1, 2, 3)]

    def test_point_none(self) -> None:
        result = list(coords(Point()))
        assert result == []

    def test_multipoint(self) -> None:
        result = list(coords(MultiPoint([[0, 0], [1, 1]])))
        assert result == [(0, 0), (1, 1)]

    def test_linestring(self) -> None:
        result = list(coords(LineString([[0, 0], [1, 1], [2, 2]])))
        assert result == [(0, 0), (1, 1), (2, 2)]

    def test_multilinestring(self) -> None:
        result = list(coords(MultiLineString([[[0, 0], [1, 1]], [[2, 2], [3, 3]]])))
        assert result == [(0, 0), (1, 1), (2, 2), (3, 3)]

    def test_polygon(self) -> None:
        result = list(coords(Polygon([[[0, 0], [1, 0], [1, 1], [0, 0]]])))
        assert result == [(0, 0), (1, 0), (1, 1), (0, 0)]

    def test_multipolygon(self) -> None:
        result = list(coords(MultiPolygon([
            [[[0, 0], [1, 0], [1, 1], [0, 0]]],
        ])))
        assert result == [(0, 0), (1, 0), (1, 1), (0, 0)]

    def test_geometry_collection(self) -> None:
        gc = GeometryCollection(geometries=[Point([0, 0]), Point([1, 1])])
        result = list(coords(gc))
        assert result == [(0, 0), (1, 1)]

    def test_feature(self) -> None:
        f = Feature(geometry=Point([5, 6]))
        result = list(coords(f))
        assert result == [(5, 6)]

    def test_feature_null_geometry(self) -> None:
        f = Feature(geometry=None)
        result = list(coords(f))
        assert result == []

    def test_feature_collection(self) -> None:
        fc = FeatureCollection(features=[
            Feature(geometry=Point([0, 0])),
            Feature(geometry=Point([1, 1])),
        ])
        result = list(coords(fc))
        assert result == [(0, 0), (1, 1)]


class TestMapCoords:
    def test_point(self) -> None:
        p = Point([1, 2])
        result = map_coords(lambda x: x * 2, p)
        assert isinstance(result, Point)
        assert result["coordinates"] == [2, 4]

    def test_linestring(self) -> None:
        ls = LineString([[0, 0], [1, 1]])
        result = map_coords(lambda x: x + 10, ls)
        assert isinstance(result, LineString)
        assert result["coordinates"] == [[10, 10], [11, 11]]

    def test_feature(self) -> None:
        f = Feature(geometry=Point([1, 2]), properties={"name": "test"})
        result = map_coords(lambda x: x * 2, f)
        assert isinstance(result, Feature)
        assert result["geometry"]["coordinates"] == [2, 4]
        assert result["properties"]["name"] == "test"

    def test_feature_null_geometry(self) -> None:
        f = Feature(geometry=None)
        result = map_coords(lambda x: x * 2, f)
        assert result["geometry"] is None

    def test_feature_collection(self) -> None:
        fc = FeatureCollection(features=[Feature(geometry=Point([1, 2]))])
        result = map_coords(lambda x: x * 2, fc)
        assert isinstance(result, FeatureCollection)
        assert result["features"][0]["geometry"]["coordinates"] == [2, 4]

    def test_geometry_collection(self) -> None:
        gc = GeometryCollection(geometries=[Point([1, 2])])
        result = map_coords(lambda x: x * 2, gc)
        assert isinstance(result, GeometryCollection)
        assert result["geometries"][0]["coordinates"] == [2, 4]


class TestMapTuples:
    def test_point(self) -> None:
        p = Point([1, 2])
        result = map_tuples(lambda t: (t[0] + 10, t[1] + 20), p)
        assert isinstance(result, Point)
        assert result["coordinates"] == [11, 22]

    def test_linestring(self) -> None:
        ls = LineString([[0, 0], [1, 1]])
        result = map_tuples(lambda t: (t[0] + 1, t[1] + 1), ls)
        assert result["coordinates"] == [[1, 1], [2, 2]]

    def test_polygon(self) -> None:
        poly = Polygon([[[0, 0], [1, 0], [1, 1], [0, 0]]])
        result = map_tuples(lambda t: (t[0] * 2, t[1] * 2), poly)
        assert result["coordinates"] == [[[0, 0], [2, 0], [2, 2], [0, 0]]]

    def test_feature(self) -> None:
        f = Feature(geometry=Point([1, 2]))
        result = map_tuples(lambda t: (t[0] + 1, t[1] + 1), f)
        assert result["geometry"]["coordinates"] == [2, 3]


class TestMapGeometries:
    def test_single_geometry(self) -> None:
        p = Point([0, 0])
        result = map_geometries(lambda g: Point([1, 1]), p)
        assert result["coordinates"] == [1, 1]

    def test_feature(self) -> None:
        f = Feature(geometry=Point([0, 0]))
        result = map_geometries(lambda g: Point([1, 1]), f)
        assert isinstance(result, Feature)
        assert result["geometry"]["coordinates"] == [1, 1]

    def test_geometry_collection(self) -> None:
        gc = GeometryCollection(geometries=[Point([0, 0]), Point([1, 1])])
        result = map_geometries(lambda g: Point([9, 9]), gc)
        assert len(result["geometries"]) == 2
        assert result["geometries"][0]["coordinates"] == [9, 9]

    def test_feature_null_geometry(self) -> None:
        f = Feature(geometry=None)
        result = map_geometries(lambda g: Point([1, 1]), f)
        assert result["geometry"] is None


class TestMerge:
    def test_merge_features(self) -> None:
        f1 = Feature(geometry=Point([0, 0]))
        f2 = Feature(geometry=Point([1, 1]))
        result = merge(f1, f2)
        assert isinstance(result, FeatureCollection)
        assert len(result["features"]) == 2

    def test_merge_feature_collections(self) -> None:
        fc1 = FeatureCollection(features=[Feature(geometry=Point([0, 0]))])
        fc2 = FeatureCollection(features=[Feature(geometry=Point([1, 1]))])
        result = merge(fc1, fc2)
        assert len(result["features"]) == 2

    def test_merge_geometries(self) -> None:
        p = Point([0, 0])
        ls = LineString([[0, 0], [1, 1]])
        result = merge(p, ls)
        assert len(result["features"]) == 2
        assert result["features"][0]["geometry"]["type"] == "Point"
        assert result["features"][1]["geometry"]["type"] == "LineString"

    def test_merge_mixed(self) -> None:
        p = Point([0, 0])
        f = Feature(geometry=Point([1, 1]))
        fc = FeatureCollection(features=[Feature(geometry=Point([2, 2]))])
        result = merge(p, f, fc)
        assert len(result["features"]) == 3
