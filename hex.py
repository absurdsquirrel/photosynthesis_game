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
            raise ValueError(f"Hex coordinates must sum to 0: {self.q, self.r, self.s}")

    def __iter__(self):
        return iter((self.q, self.r, self.s))

    def __add__(self, other: Hex) -> Hex:
        if not isinstance(other, Hex):
            raise ValueError(f"addition undefined between Hex and {type(other)}")
        return Hex(
            self.q + other.q,
            self.r + other.r,
            self.s + other.s
        )

    def __sub__(self, other: Hex) -> Hex:
        if not isinstance(other, Hex):
            raise ValueError(f"subtraction undefined between Hex and {type(other)}")
        return Hex(
            self.q - other.q,
            self.r - other.r,
            self.s - other.s
        )

    def __len__(self):
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2

    def distance(self, other: Hex):
        if not isinstance(other, Hex):
            raise ValueError(f"distance undefined between Hex and {type(other)}")
        return len(self - other)

    def neighbors(self) -> list[Hex]:
        return [self + hd for hd in HEX_DIRECTIONS]

    @staticmethod
    def hex_from_str(qrs: str) -> Hex:
        """
        Create a hex from a string in the form 'q, r, s'
        Raises ValueError if the input is bad or is not a valid Hex
        """
        q, r, s, *_ = qrs.strip().split(',')
        q, r, s = int(q), int(r), int(s)
        return Hex(q, r, s)


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
