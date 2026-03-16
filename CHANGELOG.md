# Changelog

## 0.1.0

- Initial release: drop-in Python replacement for jazzband/geojson
- All 7 RFC 7946 geometry types + Feature + FeatureCollection
- JSON codec with GeoJSON object hooks (dump/dumps/load/loads)
- RFC 7946 coordinate validation (ranges, ring closure, winding order)
- `__geo_interface__` protocol support
- Coordinate utilities: coords, map_coords, map_tuples, map_geometries, merge
- Full type hints with py.typed marker
- Zero dependencies, Python 3.10+
- Package renamed from geospec to geojsonkit (PyPI name conflict)
