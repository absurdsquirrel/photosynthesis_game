from __future__ import annotations

from typing import Protocol, Iterable, Callable

from photosynthesis_board import PhotosynthesisBoard
from player import Player


class UI(Protocol):
    def display_game_board(self, board: PhotosynthesisBoard) -> None:
        raise NotImplementedError

    def display_player_board(self, player: Player) -> None:
        raise NotImplementedError

    def display_message(self, msg: str) -> None:
        raise NotImplementedError

    def prompt(
            self,
            msg: str,
            expected: Iterable[str] | None = None,
            validator: Callable[[str], bool] | None = None
    ) -> str:
        raise NotImplementedError
