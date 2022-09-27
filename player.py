from dataclasses import dataclass, field


@dataclass
class Player:
    """
    TODO:
        clean this up, handle 'available' pieces
        figure out a solution to cyclic dependency w/ Tree
        should Player be a behavior-driven class?
    """
    name: str
    light_points: int = field(init=False, default=0)
    seeds: int = field(init=False, default=6)
    small_trees: int = field(init=False, default=8)
    medium_trees: int = field(init=False, default=4)
    tall_trees: int = field(init=False, default=2)

    def buy(self, ):
        # TODO: logic for buying seeds/trees
        ...
    """
    Buying: Players can use their light points to
    purchase seeds or trees of any size from their Player
    Boards. The numbers next to them correspond to their
    value in light points. They must buy from the bottom
    of the board up, in any column (from the least to the
    most expensive). Once a player has bought the pieces
    needed, and subtracted the value in light points using
    the tracker, the pieces are moved to the available area
    next to the Player Board.

    Note: The 2 Seeds, 2 Small Trees, and 1 Medium Tree left
    in the available area at the end of the set up are available
    to plant without buying, in future rounds. Any other
    seeds and trees a player wishes to use from their Player
    Board must be bought, and then placed in the available area.
    """
