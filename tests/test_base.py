"""Tests for the GeoJSON base class."""

from geojsonkit.base import GeoJSON


class TestGeoJSON:
    def test_type_set_from_class_name(self) -> None:
        obj = GeoJSON()
        assert obj["type"] == "GeoJSON"

    def test_attribute_access_read(self) -> None:
        obj = GeoJSON(foo="bar")
        assert obj.foo == "bar"

    def test_attribute_access_write(self) -> None:
        obj = GeoJSON()
        obj.foo = "bar"
        assert obj["foo"] == "bar"

    def test_attribute_access_delete(self) -> None:
        obj = GeoJSON(foo="bar")
        del obj.foo
        assert "foo" not in obj

    def test_attribute_error_on_missing(self) -> None:
        obj = GeoJSON()
        try:
            _ = obj.nonexistent
            assert False, "Should have raised AttributeError"
        except AttributeError:
            pass

    def test_delete_attribute_error_on_missing(self) -> None:
        obj = GeoJSON()
        try:
            del obj.nonexistent
            assert False, "Should have raised AttributeError"
        except AttributeError:
            pass

    def test_geo_interface(self) -> None:
        obj = GeoJSON(foo="bar")
        iface = obj.__geo_interface__
        assert isinstance(iface, dict)
        assert iface["type"] == "GeoJSON"
        assert iface["foo"] == "bar"
        # Must be a plain dict, not the same object
        assert type(iface) is dict

    def test_repr(self) -> None:
        obj = GeoJSON(foo=1)
        r = repr(obj)
        assert r.startswith("GeoJSON(")
        assert "foo" in r

    def test_is_valid_delegates(self) -> None:
        obj = GeoJSON()
        # GeoJSON is not a valid type per RFC 7946
        assert not obj.is_valid

    def test_errors_delegates(self) -> None:
        obj = GeoJSON()
        errs = obj.errors()
        assert isinstance(errs, list)
        assert len(errs) > 0

    def test_dict_behavior(self) -> None:
        obj = GeoJSON(a=1, b=2)
        assert len(obj) == 3  # a, b, type
        assert "a" in obj
        assert obj.get("c", 99) == 99

    def test_extra_kwargs(self) -> None:
        obj = GeoJSON(custom="value")
        assert obj["custom"] == "value"
