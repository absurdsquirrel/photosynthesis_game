from __future__ import annotations

from typing import Callable

from hex import Hex
from photosynthesis_board import PhotosynthesisBoard, TREE
from player import Player
from asciihexprinter import HexGrid


# see ui.UI for protocol
# noinspection PyMethodMayBeStatic
class CLI:
    def __init__(self):
        self.grid = HexGrid(3, Hex(3, 3, -6))
        self.board: PhotosynthesisBoard | None = None

    def display_game_board(self, board: PhotosynthesisBoard) -> None:
        self.board = board
        for tile in board.tiles:
            player, tree = board.get_tile(tile)
            text1 = player.name if player else ""
            text2 = TREE(tree).name if tree is not None else ""
            self.grid.add_hex(tile, text1, text2)

        self.grid.print()
        # TODO: indicate sun
        # TODO: display scoring tokens
        # TODO: display sun revolution counter

    def display_player_board(self, player: Player) -> None:
        print(player.name)
        print(f"Score: {player.score}")
        print(f"Light: {player.light_points}")
        print("      \tTrees\t(cost)\tAvailable")
        for tree in TREE:
            print(
                f"{tree.name}\t{player.trees[tree]}\t\t({player.price_of(tree)})\t\t{player.available[tree]}"
            )

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

        for tile in legal_options:
            _, tree = self.board.get_tile(tile)
            text1 = f"{tile.q},{tile.r}"
            text2 = TREE(tree).name if tree is not None else ""
            self.grid.add_hex(tile, text1, text2, "%")
        self.grid.print()
        # available_hexes = [f"\n{q}, {r}, {s}" for q, r, s in legal_options]
        hex_prompt = f"""
{player} specify hex coordinates: q, r
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
            f"{i}. {TREE(i).name} for {player.price_of(TREE(i))} light"
            for i in range(4) if i in legal_options
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
