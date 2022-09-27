from gameboard import GameBoard
from hex import Hex
from player import Player
from tree import Tree


def main():
    gb = GameBoard()
    player1 = Player('Player 1')
    tile = Hex(0, 0, 0)
    gb.tiles[tile] = Tree(player1, 3)
    hd = gb.sun_direction
    tile1 = tile + hd
    tile2 = tile - hd
    for i in range(2, -1, -1):
        gb.tiles[tile1] = Tree(player1, i)
        gb.tiles[tile2] = Tree(player1, i)
        tile1 = tile1 + hd
        tile2 = tile2 - hd

    for tile, tree in gb.tiles.items():
        if not tree:
            continue
        print(f"{tile, tree.height} in shadow? {gb.is_in_shadow(tile)}")


if __name__ == '__main__':
    main()
    print("Done.")
