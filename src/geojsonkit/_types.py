"""Type aliases for GeoJSON coordinate types."""

from __future__ import annotations

from typing import TypeAlias, Union

Coord2D: TypeAlias = tuple[float, float]
Coord3D: TypeAlias = tuple[float, float, float]
Position: TypeAlias = Union[Coord2D, Coord3D]

BBox2D: TypeAlias = tuple[float, float, float, float]
BBox3D: TypeAlias = tuple[float, float, float, float, float, float]
BBox: TypeAlias = Union[BBox2D, BBox3D]
