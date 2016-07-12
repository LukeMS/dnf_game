from pygame import Rect

from constants import TILE_W, TILE_H, GAME_COLORS
from game_types import Position


class Tile:
    """a tile of the map and its properties"""

    _base = {
        "block_mov": False,
        "block_sight": False,
        "id": ord("."),
        "color": None
    }

    templates = {
        "floor": {
            "color": (129, 106, 86)
        },
        "wall": {
            "block_mov": True,
            "block_sight": True,
            "id": ord("#"),
            "color": (161, 161, 161)
        },
        "water": {
            "id": ord("="),
            "color": GAME_COLORS["blue"]
        }
    }

    def __init__(self, pos, template,
                 block_mov=None, block_sight=None,
                 id=None, color=None):
        self.name = template

        component = dict(self._base)
        component.update(self.templates[template])
        if block_mov is not None:
            component["block_mov"] = block_mov
        component["block_sight"] = block_sight or component["block_sight"]
        component["id"] = id or component["id"]
        component["color"] = color or component["color"]

        for key, value in component.items():
            setattr(self, key, value)

        self.visible = False
        self.explored = False
        self.tiling_index = 0
        self.tile_variation = 0
        self.max_var = 0

        x, y = pos
        self.rect = Rect(x, y, TILE_W, TILE_H)

    @property
    def pos(self):
        return Position((self.rect.x, self.rect.y))

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    def __floordiv__(self, n):
        try:
            return Position(int(self.x // n[0]), int(self.y // n[1]))
        except TypeError:
            return Position(int(self.x // n), int(self.y // n))
