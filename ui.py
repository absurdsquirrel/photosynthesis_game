from __future__ import annotations

from typing import Protocol, Iterable, Callable

from hex import Hex
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

    def prompt_for_hex(
            self, player: Player,
            legal_options: Iterable[Hex] | None = None,
            cancel: str | None = ''
    ) -> Hex | None:
        raise NotImplementedError

    def prompt_for_tree(self, player: Player,
                        legal_options: Iterable[int]) -> int | None:
        raise NotImplementedError
