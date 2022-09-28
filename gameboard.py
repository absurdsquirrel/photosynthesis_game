"""
Board generation algorithm adapted from:
https://stackoverflow.com/a/2093442
"""
from __future__ import annotations

from hex import Hex, HEX_DIRECTIONS


class GameBoard:
    def __init__(self, radius: int):
        self.tiles: dict[Hex, tuple | None] = {}
        self._generate_tiles(radius)

    def _generate_tiles(self, radius: int) -> None:
        for i in range(radius + 1):
            tile = Hex(-i, i, 0)
            self.tiles[tile] = None
            for hd in HEX_DIRECTIONS:
                for _ in range(i):
                    tile = tile + hd
                    self.tiles[tile] = None

    # TODO: get tiles in a range, and other ways?
