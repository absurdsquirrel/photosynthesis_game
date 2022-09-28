from __future__ import annotations

from gameboard import GameBoard
from hex import HEX_DIRECTIONS, Hex
from player import Player


class PhotosynthesisBoard(GameBoard):
    def __init__(self):
        super().__init__(3)
        self.round = 0
        self.sun_direction = HEX_DIRECTIONS[0]

    def advance_round(self) -> bool:
        """
        Move the sun to the next position.
        Returns True when the sun completes a full revolution.
        """
        self.round = (self.round + 1) % 6
        # index by negative round because DIRECTIONS is CCW
        self.sun_direction = HEX_DIRECTIONS[-self.round]
        return not self.round

    def is_in_shadow(self, tile: Hex) -> bool:
        _, tree = self.get_tile(tile)
        if not tree:
            raise ValueError(f"{tile} does not have a piece on it.")
        for _ in range(3):
            tile = tile + self.sun_direction
            if tile not in self.tiles:
                # crossed edge of board
                return False
            _, tree2 = self.get_tile(tile)
            if tree2 and tree2 >= tree:
                return True
        return False

    def get_tile(
            self, tile: Hex
    ) -> tuple[Player, int] | tuple[None, None]:
        if tile not in self.tiles:
            raise ValueError(f"{tile} is not on the board.")
        if not self.tiles[tile]:
            return None, None
        return self.tiles[tile]

    def set_tile(
            self,
            tile: Hex,
            player: Player | None,
            tree: int | None
    ) -> None:
        if tile not in self.tiles:
            raise ValueError(f"{tile} is not on the board.")
        if not player or tree is None:
            self.tiles[tile] = None
        else:
            self.tiles[tile] = (player, tree)

    def get_player_tiles(self, player: Player) -> list[tuple[Hex, int]]:
        return [
            (tile, contents[1]) for tile, contents in self.tiles
            if contents and contents[0] is player
        ]
