"""Tests for Feature and FeatureCollection."""

from geojsonkit import Feature, FeatureCollection, Point


class TestFeature:
    def test_create_with_geometry(self) -> None:
        f = Feature(geometry=Point([0, 0]))
        assert f["type"] == "Feature"
        assert f["geometry"]["type"] == "Point"
        assert f["properties"] == {}

    def test_with_properties(self) -> None:
        f = Feature(geometry=Point([0, 0]), properties={"name": "test"})
        assert f["properties"]["name"] == "test"

    def test_with_id(self) -> None:
        f = Feature(id="abc", geometry=Point([0, 0]))
        assert f["id"] == "abc"

    def test_no_id_when_none(self) -> None:
        f = Feature(geometry=Point([0, 0]))
        assert "id" not in f

    def test_null_geometry(self) -> None:
        f = Feature(geometry=None)
        assert f["geometry"] is None
        assert f.is_valid

    def test_default_properties(self) -> None:
        f = Feature()
        assert f["properties"] == {}

    def test_attribute_access(self) -> None:
        f = Feature(geometry=Point([0, 0]), properties={"name": "x"})
        assert f.type == "Feature"
        assert f.geometry["type"] == "Point"
        assert f.properties["name"] == "x"

    def test_extra_kwargs(self) -> None:
        f = Feature(geometry=Point([0, 0]), bbox=[0, 0, 1, 1])
        assert f["bbox"] == [0, 0, 1, 1]

    def test_is_valid(self) -> None:
        f = Feature(geometry=Point([0, 0]))
        assert f.is_valid

    def test_geo_interface(self) -> None:
        f = Feature(geometry=Point([0, 0]))
        iface = f.__geo_interface__
        assert iface["type"] == "Feature"
        assert "geometry" in iface
        assert "properties" in iface


class TestFeatureCollection:
    def test_create(self) -> None:
        fc = FeatureCollection(features=[
            Feature(geometry=Point([0, 0])),
            Feature(geometry=Point([1, 1])),
        ])
        assert fc["type"] == "FeatureCollection"
        assert len(fc["features"]) == 2

    def test_empty(self) -> None:
        fc = FeatureCollection()
        assert fc["features"] == []
        assert fc.is_valid

    def test_attribute_access(self) -> None:
        fc = FeatureCollection(features=[Feature(geometry=Point([0, 0]))])
        assert fc.type == "FeatureCollection"
        assert len(fc.features) == 1

    def test_is_valid(self) -> None:
        fc = FeatureCollection(features=[Feature(geometry=Point([0, 0]))])
        assert fc.is_valid

    def test_extra_kwargs(self) -> None:
        fc = FeatureCollection(features=[], custom="data")
        assert fc["custom"] == "data"
