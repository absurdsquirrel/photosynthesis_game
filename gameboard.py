"""
Board generation algorithm adapted from:
https://stackoverflow.com/a/2093442
"""
from __future__ import annotations

from typing import Iterator

from hex import Hex, HEX_DIRECTIONS


class GameBoard:
    def __init__(self, radius: int):
        self._tiles: dict[Hex, tuple | None] = {}
        self._generate_tiles(radius)

    def _generate_tiles(self, radius: int) -> None:
        for i in range(radius + 1):
            tile = Hex(-i, i, 0)
            self._tiles[tile] = None
            for hd in HEX_DIRECTIONS:
                for _ in range(i):
                    tile = tile + hd
                    self._tiles[tile] = None

    # TODO: get tiles in a range, and other ways?
    def get_tiles_in_range(self, origin: Hex, tile_range: range) -> Iterator[Hex]:
        """
        Returns an iterator of tiles within a specified range from the origin.
        If tile_range includes 0, the origin will be included in the list.
        """
        if origin not in self._tiles:
            raise ValueError(f"{origin} is not on the board.")
        # return[
        #     tile for tile in self._tiles
        #     if origin.distance(tile) in tile_range
        # ]
        for tile in self._tiles:
            if origin.distance(tile) in tile_range:
                yield tile
