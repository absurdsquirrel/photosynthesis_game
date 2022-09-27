from __future__ import annotations

from hex import Hex, HEX_DIRECTIONS
from player import Player
from tree import Tree


class GameBoard:
    # TODO: generalize this class and implement Photosynthesis in a subclass
    def __init__(self):
        self.tiles: dict[Hex, Tree | None] = {}
        self.sun_direction: Hex = HEX_DIRECTIONS[0]
        self._generate_tiles()

    def is_in_shadow(self, tile: Hex) -> bool:
        tree = self.tiles.get(tile)
        if not tree:
            msg = f"{tile} must be on the board and have a tree."
            raise ValueError(msg)
        for _ in range(3):
            tile = tile + self.sun_direction
            if tile not in self.tiles:
                # crossed edge of board
                return False
            tile2 = self.tiles[tile]
            if tile2 and tile2.height >= tree.height:
                return True
        return False

    def _generate_tiles(self) -> None:
        # this algorithm doesn't generalize to an arbitrary radius
        # and there's some duplicate work where neighbors overlap
        # but it gets the job done for a photosynthesis board
        # TODO: generalize algorithm. See: https://stackoverflow.com/a/2093442
        tile = Hex(0, 0, 0)
        self.tiles[tile] = None
        for neighbor in tile.neighbors():
            self.tiles[neighbor] = None
        for hd in HEX_DIRECTIONS:
            tile = Hex(
                2 * hd.q,
                2 * hd.r,
                2 * hd.s,
            )
            self.tiles[tile] = None
            for neighbor in tile.neighbors():
                self.tiles[neighbor] = None

    def play_seed(self, player: Player, tile: Hex) -> None:
        if player.seeds < 1:
            raise ValueError(f"{player.name} is out of seeds")
        player.seeds -= 1
        seed = Tree(player, 0)
        self.tiles[tile] = seed
