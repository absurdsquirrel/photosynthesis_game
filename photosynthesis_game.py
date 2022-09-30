from __future__ import annotations

from collections import deque
from enum import IntEnum
from functools import partial
from typing import Iterable

from hex import Hex
from photosynthesis_board import PhotosynthesisBoard
from player import Player
from ui import UI


# this is probably unnecessary, but it's a helpful reference
class TREE(IntEnum):
    SEED = 0
    SMALL = 1
    MEDIUM = 2
    TALL = 3


class PhotosynthesisGame:
    def __init__(
            self,
            number_of_players: int,
            ui: UI,
            advanced: bool = False
    ):
        if number_of_players < 2 or number_of_players > 4:
            raise ValueError("Photosynthesis is a game for 2-4 players.")

        self.ui = ui

        self.board = PhotosynthesisBoard()
        self.sun_revolution_counter = 3 if not advanced else 4
        self.can_activate_in_shade = not advanced

        self.scoring_tokens: list[list[int]] = [
            [20, 21, 22],
            [17, 17, 18, 18, 19],
            [13, 13, 14, 14, 16, 16, 17],
            [12, 12, 12, 12, 13, 13, 13, 14, 14]
        ]

        if number_of_players < 3:
            self.scoring_tokens[0] = []

        # TODO: get names from UI
        self.players = deque([
            Player(f"Player {i}") for i in range(1, number_of_players + 1)
        ])

        self.play_game()

    def play_game(self) -> None:
        self.place_starting_trees()
        while self.sun_revolution_counter > 0:
            self.photosynthesis()
            for player in self.players:
                self.life_cycle(player)
            self.advance_starting_player()
            if self.board.advance_round():
                self.sun_revolution_counter -= 1
        self.end_game()

    def place_starting_trees(self):
        for _ in range(2):
            for player in self.players:
                legal_options = self.board.get_empty_tiles_in_range(
                    Hex(0, 0, 0), range(3, 4)
                )
                tile = self.prompt_for_hex(player, legal_options, cancel=None)
                player.use_available(TREE.SMALL)
                self.board.set_tile(tile, player, TREE.SMALL)

    def advance_starting_player(self) -> None:
        """
        The next player in order gets to go first in the following round.
        """
        self.players.append(self.players.popleft())

    def photosynthesis(self) -> None:
        """Players gain light points for trees receiving sunlight"""
        for player in self.players:
            player_tiles = self.board.get_player_tiles(player)
            player.light_points += sum([
                tree for tile, tree in player_tiles
                if tree and not self.board.is_in_shadow(tile)
            ])

    @staticmethod
    def hex_validator(qrs: str, legal_options: Iterable[Hex] | None = None) -> bool:
        try:
            _hex = Hex.hex_from_str(qrs)
        except ValueError:
            return False
        return _hex in legal_options

    def prompt_for_hex(
            self, player: Player,
            legal_options: Iterable[Hex] | None = None,
            cancel: str | None = ''
    ) -> Hex | None:
        validator = partial(self.hex_validator, legal_options=legal_options)
        hex_prompt = f"""
{player} specify hex coordinates: q, r, s
"""
        qrs = self.ui.prompt(
                hex_prompt,
                expected=[''],  # option to cancel
                validator=validator
        )
        if cancel is not None and qrs == cancel:
            return None
        return Hex.hex_from_str(qrs)

    def collect(self, player: Player, activated_tiles: set[Hex]) -> None:
        """
        Player scores points for ending the life-cycle of
        one of their tall trees. Points scored depends on the
        quality of the soil and remaining score tokens.
        """
        legal_options = {
            tile for tile, _ in
            self.board.get_player_tiles(player, tree_range=range(3, 4))
            if tile not in activated_tiles
        }
        if not legal_options:
            self.ui.display_message("Nothing to collect.")
            return
        tile = self.prompt_for_hex(player, legal_options=legal_options)
        if tile is None:  # cancel action
            return
        activated_tiles.add(tile)
        soil_quality = len(tile)
        while not self.scoring_tokens[soil_quality] and soil_quality < 4:
            soil_quality += 1
        points = self.scoring_tokens[soil_quality].pop()
        player.score += points
        self.board.set_tile(tile, None, None)
        player.recover_tree(TREE.TALL)
        if all(len(stack) < 1 for stack in self.scoring_tokens):
            self.ui.display_message("Out of scoring tokens.")
            self.end_game()

    def buy(self, player: Player) -> None:
        ...

    def plant(self, player: Player, activated_tiles: set[Hex]) -> None:
        ...

    def grow(self, player: Player, activated_tiles: set[Hex]) -> None:
        ...

    def life_cycle(self, player: Player) -> None:
        action_prompt = f"""
{player}'s turn.
Actions:
    1. Buy seeds or trees
    2. Plant a seed
    3. Grow a tree
    4. Collect points for a tall tree
    5. End Turn
"""
        expected = ['1', '2', '3', '4', '5']
        activated_tiles: set[Hex] = set()
        player_action = self.ui.prompt(action_prompt, expected=expected)
        while player_action != '5':
            if player_action == '1':
                self.buy(player)
            elif player_action == '2':
                self.plant(player, activated_tiles)
            elif player_action == '3':
                self.grow(player, activated_tiles)
            elif player_action == '4':
                self.collect(player, activated_tiles)
            else:
                break
            player_action = self.ui.prompt(action_prompt, expected=expected)

    def end_game(self):
        # players score an extra point for every 3 unused light
        top_score = 0
        for player in self.players:
            player.score += player.light_points // 3
            top_score = max(top_score, player.score)
        winners = [player.name for player in self.players if player.score == top_score]
        self.ui.display_message(f"""
Winner{'s' if len(winners) > 1 else ''}: {', '.join(winners)} with {top_score} points. 
""")
        quit()
