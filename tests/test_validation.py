"""Tests for RFC 7946 validation."""

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
)
from geojsonkit.validation import errors, is_valid


class TestIsValid:
    def test_valid_point(self) -> None:
        assert is_valid(Point([0, 0]))

    def test_invalid_point(self) -> None:
        assert not is_valid(Point([200, 0]))


class TestErrors:
    def test_missing_type(self) -> None:
        errs = errors({})
        assert any("type" in e for e in errs)

    def test_invalid_type(self) -> None:
        errs = errors({"type": "Bogus"})
        assert any("not a valid GeoJSON type" in e for e in errs)


class TestPointValidation:
    def test_valid(self) -> None:
        assert errors(Point([0, 0])) == []

    def test_valid_3d(self) -> None:
        assert errors(Point([0, 0, 100])) == []

    def test_longitude_out_of_range(self) -> None:
        errs = errors(Point([181, 0]))
        assert any("Longitude" in e for e in errs)

    def test_latitude_out_of_range(self) -> None:
        errs = errors(Point([0, 91]))
        assert any("Latitude" in e for e in errs)

    def test_too_few_values(self) -> None:
        errs = errors({"type": "Point", "coordinates": [0]})
        assert any("2 or 3" in e for e in errs)

    def test_too_many_values(self) -> None:
        errs = errors({"type": "Point", "coordinates": [0, 0, 0, 0]})
        assert any("2 or 3" in e for e in errs)

    def test_null_coordinates(self) -> None:
        p = Point()
        assert errors(p) == []

    def test_missing_coordinates(self) -> None:
        errs = errors({"type": "Point"})
        assert any("coordinates" in e for e in errs)

    def test_boundary_values(self) -> None:
        assert errors(Point([-180, -90])) == []
        assert errors(Point([180, 90])) == []


class TestMultiPointValidation:
    def test_valid(self) -> None:
        assert errors(MultiPoint([[0, 0], [1, 1]])) == []

    def test_invalid_position(self) -> None:
        errs = errors(MultiPoint([[200, 0]]))
        assert any("Longitude" in e for e in errs)


class TestLineStringValidation:
    def test_valid(self) -> None:
        assert errors(LineString([[0, 0], [1, 1]])) == []

    def test_too_few(self) -> None:
        errs = errors(LineString([[0, 0]]))
        assert any("at least 2" in e for e in errs)


class TestMultiLineStringValidation:
    def test_valid(self) -> None:
        assert errors(MultiLineString([[[0, 0], [1, 1]]])) == []

    def test_inner_too_few(self) -> None:
        errs = errors(MultiLineString([[[0, 0]]]))
        assert any("at least 2" in e for e in errs)


class TestPolygonValidation:
    def test_valid(self) -> None:
        assert errors(Polygon([[[0, 0], [1, 0], [1, 1], [0, 0]]])) == []

    def test_unclosed_ring(self) -> None:
        errs = errors(Polygon([[[0, 0], [1, 0], [1, 1], [0, 1]]]))
        assert any("not closed" in e for e in errs)

    def test_ring_too_few(self) -> None:
        errs = errors(Polygon([[[0, 0], [1, 0], [0, 0]]]))
        assert any("at least 4" in e for e in errs)


class TestMultiPolygonValidation:
    def test_valid(self) -> None:
        assert errors(MultiPolygon([[[[0, 0], [1, 0], [1, 1], [0, 0]]]])) == []

    def test_inner_invalid(self) -> None:
        errs = errors(MultiPolygon([[[[0, 0], [1, 0], [0, 0]]]]))
        assert any("at least 4" in e for e in errs)


class TestGeometryCollectionValidation:
    def test_valid(self) -> None:
        gc = GeometryCollection(geometries=[Point([0, 0])])
        assert errors(gc) == []

    def test_missing_geometries(self) -> None:
        errs = errors({"type": "GeometryCollection"})
        assert any("geometries" in e for e in errs)

    def test_nested_invalid(self) -> None:
        gc = GeometryCollection(geometries=[Point([200, 0])])
        errs = errors(gc)
        assert any("geometries[0]" in e for e in errs)


class TestFeatureValidation:
    def test_valid(self) -> None:
        f = Feature(geometry=Point([0, 0]))
        assert errors(f) == []

    def test_null_geometry_valid(self) -> None:
        f = Feature(geometry=None)
        assert errors(f) == []

    def test_missing_geometry(self) -> None:
        errs = errors({"type": "Feature", "properties": {}})
        assert any("geometry" in e for e in errs)

    def test_missing_properties(self) -> None:
        errs = errors({"type": "Feature", "geometry": None})
        assert any("properties" in e for e in errs)

    def test_invalid_geometry(self) -> None:
        f = Feature(geometry=Point([200, 0]))
        errs = errors(f)
        assert any("geometry:" in e for e in errs)


class TestFeatureCollectionValidation:
    def test_valid(self) -> None:
        fc = FeatureCollection(features=[Feature(geometry=Point([0, 0]))])
        assert errors(fc) == []

    def test_empty_valid(self) -> None:
        fc = FeatureCollection(features=[])
        assert errors(fc) == []

    def test_missing_features(self) -> None:
        errs = errors({"type": "FeatureCollection"})
        assert any("features" in e for e in errs)

    def test_nested_invalid(self) -> None:
        fc = FeatureCollection(features=[Feature(geometry=Point([200, 0]))])
        errs = errors(fc)
        assert any("features[0]" in e for e in errs)
