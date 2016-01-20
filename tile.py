from pygame import Rect

from constants import TILE_W, TILE_H
from game_types import Position


class Tile:
    # a tile of the map and its properties
    def __init__(self, block_mov, pos, block_sight=None, id=0):
        self.block_mov = block_mov

        # by default, if a tile is block_mov, it also blocks sight
        if block_sight is None:
            block_sight = block_mov
        self.block_sight = block_sight

        self.id = id
        self.visible = False
        self.explored = False

        x, y = pos
        self.rect = Rect(x, y, TILE_W, TILE_H)

    @property
    def pos(self):
        return Position(self.rect.x, self.rect.y)

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    def __floordiv__(self, n):
        if isinstance(n, tuple):
            return Position(int(self.x // n[0]), int(self.y // n[1]))
        elif isinstance(n, (int, float)):
            return Position(int(self.x // n), int(self.y // n))


class Floor(Tile):
    def __init__(
        self, pos, block_mov=False, block_sight=None, id=ord(".")
    ):
        super().__init__(
            pos=pos,
            block_mov=block_mov,
            block_sight=block_sight,
            id=id)
        self.name = 'floor'


class Wall(Tile):
    def __init__(
        self, pos, block_mov=True, block_sight=True, id=ord("#")
    ):
        super().__init__(
            pos=pos,
            block_mov=block_mov,
            block_sight=block_sight,
            id=id)
        self.name = 'wall'
