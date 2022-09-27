from dataclasses import dataclass, field
from uuid import UUID, uuid4

from player import Player


@dataclass(frozen=True)
class Tree:
    player: Player
    height: int

    # to avoid hash collisions so Trees can be dict keys
    id: UUID = field(
        init=False,
        repr=False,
        default_factory=uuid4
    )