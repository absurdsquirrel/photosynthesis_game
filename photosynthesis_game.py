from __future__ import annotations

from collections import deque
from enum import IntEnum

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
        self.can_plant_or_grow_in_shade = not advanced

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

        # TODO: setup 2 small trees per player

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
    def hex_validator(qrs: str) -> bool:
        try:
            _hex = Hex.hex_from_str(qrs)
        except ValueError:
            return False
        return isinstance(_hex, Hex) and len(_hex) < 4

    def prompt_for_hex(self, player) -> Hex:
        hex_prompt = f"""
{player} specify hex coordinates: q, r, s
"""
        qrs = self.ui.prompt(
                hex_prompt,
                validator=self.hex_validator
        )
        return Hex.hex_from_str(qrs)

    def collect(self, player: Player) -> None:
        """
        Player scores points for ending the life-cycle of
        one of their tall trees. Points scored depends on the
        quality of the soil and remaining score tokens.
        """
        tile = self.prompt_for_hex(player)
        p, t = self.board.get_tile(tile)
        if p is not player:
            raise ValueError(f"{player} does not control {tile}")
        if t != TREE.TALL:
            raise ValueError(f"{tile} does not have a tall tree.")
        soil_quality = len(tile)
        while not self.scoring_tokens[soil_quality] and soil_quality < 4:
            soil_quality += 1
        if soil_quality > 3:
            raise ValueError("Ran out of score tokens.")
        points = self.scoring_tokens[soil_quality].pop()
        player.score += points
        self.board.set_tile(tile, None, None)
        player.recover_tree(TREE.TALL)

    def buy(self, player: Player) -> None:
        ...

    def plant(self, player: Player) -> None:
        ...

    def grow(self, player: Player) -> None:
        ...

    def life_cycle(self, player: Player) -> None:
        activated_tiles: set[Hex] = set()
        player_tiles = self.board.get_player_tiles(player)
        opponent_tiles = {
            opponent.name: self.board.get_player_tiles(opponent)
            for opponent in self.players if opponent is not player
        }

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
        player_action = self.ui.prompt(action_prompt, expected=expected)
        while player_action != '5':
            if player_action == '1':
                self.buy(player)
            elif player_action == '2':
                self.plant(player)
            elif player_action == '3':
                self.grow(player)
            elif player_action == '4':
                self.collect(player)
            else:
                break
            player_action = self.ui.prompt(action_prompt, expected=expected)
