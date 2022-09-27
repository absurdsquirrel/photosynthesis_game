"""
Portions of this code adapted from:
https://www.redblobgames.com/grids/hexagons/codegen/output/lib.py
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Hex:
    q: int
    r: int
    s: int

    def __post_init__(self):
        if sum((self.q, self.r, self.s)) != 0:
            raise ValueError(f"Hex coordinates must sum to 0.")

    @property
    def soil_value(self) -> int:
        # TODO: this belong in a subclass for Photosynthesis
        return 4 - len(self)

    def __add__(self, other: Hex) -> Hex:
        assert isinstance(other, Hex)
        return Hex(
            self.q + other.q,
            self.r + other.r,
            self.s + other.s
        )

    def __sub__(self, other: Hex) -> Hex:
        assert isinstance(other, Hex)
        return Hex(
            self.q - other.q,
            self.r - other.r,
            self.s - other.s
        )

    def __len__(self):
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2

    def distance(self, other: Hex):
        assert isinstance(other, Hex)
        return len(self - other)

    def neighbors(self) -> list[Hex]:
        return [self + hd for hd in HEX_DIRECTIONS]


# directions & diagonals start E/ENE of the r=0 line and go CCW
HEX_DIRECTIONS = (
    Hex(1, 0, -1),
    Hex(1, -1, 0),
    Hex(0, -1, 1),
    Hex(-1, 0, 1),
    Hex(-1, 1, 0),
    Hex(0, 1, -1)
)

# Probably not needed, but keeping it here anyway
HEX_DIAGONALS = (
    Hex(2, -1, -1),
    Hex(1, -2, 1),
    Hex(-1, -1, 2),
    Hex(-2, 1, 1),
    Hex(-1, 2, -1),
    Hex(1, 1, -2)
 )
