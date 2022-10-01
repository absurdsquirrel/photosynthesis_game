from cli import CLI
from photosynthesis_game import PhotosynthesisGame


def main():
    # noinspection PyTypeChecker
    game = PhotosynthesisGame(2, CLI())


if __name__ == '__main__':
    main()
    print("Done.")
