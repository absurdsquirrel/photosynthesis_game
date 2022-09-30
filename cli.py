from __future__ import annotations

from typing import Iterable, Callable

from hex import Hex
from photosynthesis_board import PhotosynthesisBoard, TREE
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
            expected: list[str] | None = None,
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

    def prompt_for_hex(
            self, player: Player,
            legal_options: set[Hex] | None = None,
            cancel: str | None = ''
    ) -> Hex | None:
        def validator(qrs: str) -> bool:
            try:
                _hex = Hex.hex_from_str(qrs)
            except ValueError:
                return False
            return _hex in legal_options

        hex_prompt = f"""
{player} specify hex coordinates: q, r, s
"""
        response = self.prompt(
            hex_prompt,
            expected=[cancel] if cancel is not None else None,
            validator=validator
        )
        if cancel is not None and response == cancel:
            return None
        return Hex.hex_from_str(response)

    def prompt_for_tree(self, player: Player,
                        legal_options: set[int]) -> int | None:

        legal_trees = "\n".join((
            f"{i}. {TREE(i).name}" for i in range(4) if i in legal_options
        ))

        tree_prompt = f"""
{player} select a tree:
{legal_trees}
"""
        cancel = ''
        expected = [cancel] + [str(i) for i in range(4) if i in legal_options]
        response = self.prompt(tree_prompt, expected=expected)
        if response == cancel:
            return None
        return int(response)
