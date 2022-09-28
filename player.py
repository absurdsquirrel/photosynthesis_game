from __future__ import annotations

from typing import Callable

from hex import Hex
from player_board import PlayerBoard


class Player:
    def __init__(self, name: str):
        self.name = name
        self.player_board = PlayerBoard()

    def life_cycle(
            self,
            activated_tiles: set[Hex],
            my_tiles: list[tuple[Hex, int]],
            opponent_tiles: dict[str, list[tuple[Hex, int]]]
    ) -> tuple[Callable, dict[str, ...]] | None:
        ...
