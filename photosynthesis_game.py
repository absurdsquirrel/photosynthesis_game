from __future__ import annotations

from enum import IntEnum

from gameboard import GameBoard
from hex import Hex, HEX_DIRECTIONS
from photosynthesis_board import PhotosynthesisBoard
from player import Player
from player_board import PlayerBoard


# this is probably unnecessary, but it's a helpful reference
class Tree(IntEnum):
    SEED = 0
    SMALL = 1
    MEDIUM = 2
    TALL = 3


class PhotosynthesisGame:
    """
    Things for this class TODO:
        keep track of the round (game ends after 3 or 4 rounds)
        keep track of the turn (which player gets to take actions during a round)
        keep track of 'activated tiles' during a turn
        pass information between players and the board
    """
    def __init__(self, number_of_players: int, advanced: bool = False):
        if number_of_players < 2 or number_of_players > 4:
            raise ValueError("Photosynthesis is a game for 2-4 players.")

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
        self.players = [
            Player(f"Player {i}") for i in range(1, number_of_players + 1)
        ]

    def photosynthesis(self) -> None:
        """Players gain light points for trees receiving sunlight"""
        for player in self.players:
            player_tiles = self.board.get_player_tiles(player)
            player.player_board.light_points += sum([
                tree for tile, tree in player_tiles
                if tree and not self.board.is_in_shadow(tile)
            ])

    def score_points(self, player: Player, tile: Hex) -> None:
        soil_quality = len(tile)
        while not self.scoring_tokens[soil_quality] and soil_quality < 4:
            soil_quality += 1
        if soil_quality > 3:
            raise ValueError("Ran out of score tokens.")
        points = self.scoring_tokens[soil_quality].pop()
        player.player_board.score += points

    def life_cycle(self, player: Player) -> None:
        activated_tiles: set[Hex] = set()
        player_tiles = self.board.get_player_tiles(player)
        opponent_tiles = {
            opponent.name: self.board.get_player_tiles(opponent)
            for opponent in self.players if opponent is not player
        }
        while player_action := player.life_cycle(
            activated_tiles,
            player_tiles,
            opponent_tiles
        ):
            action, kwargs = player_action
            tile: Hex | None = kwargs.get('tile')
            if tile and tile not in activated_tiles:
                activated_tiles.add(tile)
            elif tile:
                raise ValueError(f"{tile} has already been activated this turn.")
            action(player, **kwargs)
