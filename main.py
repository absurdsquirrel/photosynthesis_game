from photosynthesis_game import PhotosynthesisBoard
from collections import Counter


def main():
    gb = PhotosynthesisBoard()
    assert len(gb.tiles) == 37, f"{len(gb.tiles)}"
    assert all(len(tile) < 4 for tile in gb.tiles)
    c = Counter([len(tile) for tile in gb.tiles])
    print(c)
    assert all(c[i] == max(1, 6 * i) for i in range(4))


if __name__ == '__main__':
    main()
    print("Done.")
