"""Tests for geometry types."""

import pytest

from geojsonkit import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)


class TestPoint:
    def test_create(self) -> None:
        p = Point([-115.81, 37.24])
        assert p["type"] == "Point"
        assert p["coordinates"] == [-115.81, 37.24]

    def test_attribute_access(self) -> None:
        p = Point([0, 0])
        assert p.type == "Point"
        assert p.coordinates == [0, 0]

    def test_precision(self) -> None:
        p = Point([1.123456789, 2.987654321], precision=2)
        assert p["coordinates"] == [1.12, 2.99]

    def test_default_precision(self) -> None:
        p = Point([1.1234567, 2.9876543])
        assert p["coordinates"] == [1.123457, 2.987654]

    def test_3d(self) -> None:
        p = Point([1.0, 2.0, 100.0])
        assert len(p["coordinates"]) == 3
        assert p["coordinates"][2] == 100.0

    def test_none_coordinates(self) -> None:
        p = Point()
        assert p["coordinates"] is None

    def test_is_valid(self) -> None:
        p = Point([0, 0])
        assert p.is_valid

    def test_invalid_range(self) -> None:
        p = Point([200, 0])
        assert not p.is_valid

    def test_validate_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid Point"):
            Point([200, 0], validate=True)

    def test_extra_kwargs(self) -> None:
        p = Point([0, 0], bbox=[-1, -1, 1, 1])
        assert p["bbox"] == [-1, -1, 1, 1]

    def test_geo_interface(self) -> None:
        p = Point([0, 0])
        iface = p.__geo_interface__
        assert iface == {"type": "Point", "coordinates": [0, 0]}


class TestMultiPoint:
    def test_create(self) -> None:
        mp = MultiPoint([[0, 0], [1, 1]])
        assert mp["type"] == "MultiPoint"
        assert len(mp["coordinates"]) == 2

    def test_is_valid(self) -> None:
        mp = MultiPoint([[0, 0], [1, 1]])
        assert mp.is_valid


class TestLineString:
    def test_create(self) -> None:
        ls = LineString([[0, 0], [1, 1], [2, 2]])
        assert ls["type"] == "LineString"
        assert len(ls["coordinates"]) == 3

    def test_too_few_positions(self) -> None:
        ls = LineString([[0, 0]])
        assert not ls.is_valid
        errs = ls.errors()
        assert any("at least 2" in e for e in errs)

    def test_is_valid(self) -> None:
        ls = LineString([[0, 0], [1, 1]])
        assert ls.is_valid


class TestMultiLineString:
    def test_create(self) -> None:
        mls = MultiLineString([[[0, 0], [1, 1]], [[2, 2], [3, 3]]])
        assert mls["type"] == "MultiLineString"
        assert len(mls["coordinates"]) == 2

    def test_is_valid(self) -> None:
        mls = MultiLineString([[[0, 0], [1, 1]], [[2, 2], [3, 3]]])
        assert mls.is_valid


class TestPolygon:
    def test_create(self) -> None:
        poly = Polygon([[[0, 0], [1, 0], [1, 1], [0, 0]]])
        assert poly["type"] == "Polygon"
        assert len(poly["coordinates"]) == 1

    def test_unclosed_ring(self) -> None:
        poly = Polygon([[[0, 0], [1, 0], [1, 1], [0, 1]]])
        assert not poly.is_valid
        errs = poly.errors()
        assert any("not closed" in e for e in errs)

    def test_ring_too_few(self) -> None:
        poly = Polygon([[[0, 0], [1, 0], [0, 0]]])
        assert not poly.is_valid
        errs = poly.errors()
        assert any("at least 4" in e for e in errs)

    def test_with_hole(self) -> None:
        outer = [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]
        inner = [[2, 2], [8, 2], [8, 8], [2, 2]]  # too few? need 4+first
        poly = Polygon([outer, inner])
        # inner ring has only 4 positions which is the minimum
        assert poly["type"] == "Polygon"

    def test_is_valid(self) -> None:
        poly = Polygon([[[0, 0], [1, 0], [1, 1], [0, 0]]])
        assert poly.is_valid


class TestMultiPolygon:
    def test_create(self) -> None:
        mp = MultiPolygon([
            [[[0, 0], [1, 0], [1, 1], [0, 0]]],
            [[[2, 2], [3, 2], [3, 3], [2, 2]]],
        ])
        assert mp["type"] == "MultiPolygon"
        assert len(mp["coordinates"]) == 2

    def test_is_valid(self) -> None:
        mp = MultiPolygon([
            [[[0, 0], [1, 0], [1, 1], [0, 0]]],
        ])
        assert mp.is_valid


class TestGeometryCollection:
    def test_create(self) -> None:
        gc = GeometryCollection(geometries=[
            Point([0, 0]),
            LineString([[0, 0], [1, 1]]),
        ])
        assert gc["type"] == "GeometryCollection"
        assert len(gc["geometries"]) == 2

    def test_empty(self) -> None:
        gc = GeometryCollection()
        assert gc["geometries"] == []

    def test_is_valid(self) -> None:
        gc = GeometryCollection(geometries=[Point([0, 0])])
        assert gc.is_valid

    def test_nested_invalid(self) -> None:
        gc = GeometryCollection(geometries=[Point([200, 0])])
        assert not gc.is_valid
