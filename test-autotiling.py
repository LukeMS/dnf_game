"""An experiment to render tiles nicely (with transitions and shadows)."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pygame

import game

_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 3, 3, 0, 0, 0, 3, 0],
    [0, 3, 3, 3, 0, 0, 3, 3, 0],
    [0, 3, 3, 3, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 3, 3, 0, 0, 0, 0, 0],
    [0, 3, 0, 3, 0, 0, 0, 0, 0],
    [0, 3, 3, 3, 0, 3, 3, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def calc_tile_index_full(x0, y0):
    """Calculate the tile index based on its neighbours."""
    s = 0
    max_x = len(_map[y0]) - 1
    max_y = len(_map) - 1

    # isAboveSame
    if (y0 - 1 < 0) or (_map[y0][x0] == _map[y0 - 1][x0]):
        s += 1

    # isLeftSame
    if (x0 - 1 < 0) or (_map[y0][x0] == _map[y0][x0 - 1]):
        s += 2

    # isBelowSame
    if (y0 + 1 > max_y) or (_map[y0][x0] == _map[y0 + 1][x0]):
        s += 4

    # isRightSame
    if (x0 + 1 > max_x) or (_map[y0][x0] == _map[y0][x0 + 1]):
        s += 8

    return s


class Map(game.BaseScene):
    def __init__(self, game):
        self.game = game
        print(calc_tile_index_full(2, 2))

    def on_key_press(self, event):
        if event.key == pygame.K_ESCAPE:
            self.quit()

    def on_update(self):
        for j, y in enumerate(_map):
            for i, x in enumerate(y):
                index = calc_tile_index_full(i, j)
                self.game.gfx.draw_specific(
                    x, index, (i, j),
                    "arachne-tilesheet.png")

if __name__ == '__main__':
    from constants import TILE_W, TILE_H
    game.Game(
        scene=Map, show_fps=False,
        width=TILE_W * len(_map[0]), height=TILE_H * len(_map))
