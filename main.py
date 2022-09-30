from cli import CLI
from player import Player


def main():
    p1 = Player("Player 1")
    ui = CLI()
    ui.display_player_board(p1)


if __name__ == '__main__':
    main()
    print("Done.")
