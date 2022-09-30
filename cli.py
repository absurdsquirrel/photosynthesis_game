from __future__ import annotations

from typing import Iterable, Callable

from photosynthesis_board import PhotosynthesisBoard
from player import Player


# see ui.UI for protocol
class CLI:
    def display_game_board(self, board: PhotosynthesisBoard) -> None:
        # TODO: represent board
        raise NotImplementedError

    def display_player_board(self, player: Player) -> None:
        # TODO: represent player
        raise NotImplementedError

    def display_message(self, msg: str) -> None:
        print(msg)

    def prompt(
            self,
            msg: str, /,
            expected: Iterable[str] | None = None,
            validator: Callable[[str], bool] | None = None
    ) -> str:
        while True:
            print(msg)
            response = input("> ")
            if (
                    (expected is None and validator is None) or
                    (expected is not None and response in expected) or
                    (validator is not None and validator(response))
            ):
                return response
            print("*Invalid response. Try again.*")
