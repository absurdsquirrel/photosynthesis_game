from __future__ import annotations


class PlayerBoard:
    TREE_PRICES = (
        (2, 2, 1, 1),   # SEED
        (3, 3, 2, 2),   # SMALL
        (4, 3, 3),      # MEDIUM
        (5, 4)          # TALL
    )

    def __init__(self):
        self.score: int = 0
        self._light_points: int = 0
        self._trees: list[int] = [
            4,  # SEED
            4,  # SMALL
            1,  # MEDIUM
            2   # TALL
        ]
        self._available: list[int] = [
            2,  # SEED
            4,  # SMALL
            1,  # MEDIUM
            0   # TALL
        ]

    @property
    def trees(self) -> tuple[int]:
        return tuple(self._trees)

    @property
    def available(self) -> tuple[int]:
        return tuple(self._available)

    def price_of(self, tree: int) -> int:
        """Get the number of light points required to buy a seed/tree"""
        trees_in_stock = self._trees[tree]
        if trees_in_stock < 1:
            raise ValueError("Not enough in stock.")
        return PlayerBoard.TREE_PRICES[tree][trees_in_stock - 1]

    @property
    def light_points(self) -> int:
        return self._light_points

    @light_points.setter
    def light_points(self, points: int) -> None:
        if points < 0:
            raise ValueError(f"Not enough light points. {self._light_points}")
        self._light_points = min(points, 20)

    def buy_tree(self, tree: int) -> None:
        cost = self.price_of(tree)
        self.light_points -= cost
        self._trees[tree] -= 1
        self._available[tree] += 1

    def use_available(self, tree: int) -> None:
        if self._available[tree] < 1:
            raise ValueError("Tree not available.")
        self._available[tree] -= 1

    def recover_tree(self, tree: int) -> None:
        self._trees[tree] += 1
        self._trees[tree] = min(
            self._trees[tree],
            len(PlayerBoard.TREE_PRICES[tree])
        )

    def grow_tree(self, tree):
        if tree > 2:
            raise ValueError("Tree can't grow any bigger.")
        new_tree = tree + 1
        self.light_points -= new_tree
        self.use_available(new_tree)
        self.recover_tree(tree)
