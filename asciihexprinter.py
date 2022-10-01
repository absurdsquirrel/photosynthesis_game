"""
Generate a 2D character array to represent a hex grid.
Code adapted from:
https://github.com/cmelchior/asciihexgrid
"""
from __future__ import annotations

from hex import Hex

WIDTH = 9
HEIGHT = 5
SIDE = 2

TEMPLATE = "\n".join([
    "   _ _   ",    # 0 - 9
    " /# # #\\ ",   # 9 - 18
    "/#XXXXX#\\",   # 18 - 27
    "\\#YYYYY#/",   # 27 - 36
    " \\#_#_#/ "    # 36 - 45
])


def grid_size(hex_h: int, hex_w: int) -> tuple[int, int]:
    """
    rows, columns of character array to display the map
    """
    rows = (hex_w - 1) * HEIGHT // 2 + hex_h * HEIGHT
    cols = hex_w * (WIDTH - SIDE) + SIDE
    return rows, cols


def char_coordinates(_hex: Hex) -> tuple[int, int]:
    """
    row, column of hex in the character array
    """
    q, r, _ = _hex
    row = 2 * q + 4 * r
    col = 7 * q
    return row, col


def fit_length(text: str, length: int = 5) -> str:
    if not text:
        return " " * length
    if len(text) > length:
        return text[:length].upper()
    elif len(text) < length:
        return text.join([
            " " * ((length - len(text)) // 2 + ((length - len(text)) % 2)),
            " " * ((length - len(text)) // 2)
        ]).upper()
    else:
        return text


def hex_string(text1: str, text2: str, filler: str = ' ') -> str:
    _hex = TEMPLATE
    text1 = fit_length(text1)
    text2 = fit_length(text2)
    _hex = _hex.replace("XXXXX", text1)
    _hex = _hex.replace("YYYYY", text2)
    return _hex.replace("#", filler)


class HexGrid:
    def __init__(self, radius: int, offset: Hex = Hex(0, 0, 0)):
        self.radius = radius
        self.hex_h = self.hex_w = 2 * radius + 1
        self.rows, self.cols = grid_size(self.hex_h, self.hex_w)
        self.grid = [[' '] * self.cols for _ in range(self.rows)]
        self.offset = offset

    def add_hex(self, _hex: Hex,
                text1: str, text2: str, filler: str = ' ') -> None:
        hex_text = hex_string(text1, text2, filler)
        row, col = char_coordinates(_hex + self.offset)
        # offset for negative indicies
        # row += self.row_offset
        # col += self.col_offest
        lines = [
            line.rstrip() for line in hex_text.split("\n")
        ]

        for i, line in enumerate(lines):
            for j, ch in enumerate(line):
                r = row + i
                c = col + j
                reserved = f"\\/_{filler if filler != ' ' else ''}"
                if self.grid[r][c] not in reserved:
                    self.grid[r][c] = ch

    def print(self) -> None:
        for row in self.grid:
            line = "".join(row)
            if line.strip():
                print(line)
