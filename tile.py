"""..."""

from pygame import Rect

from constants import TILE_W, TILE_H, GAME_COLORS
from game_types import Position


class Tile:
    """A tile of the map and its properties."""

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
        "door_closed": {
            "block_mov": True,
            "block_sight": True,
            "id": ord("="),
            "color": (161, 161, 161)
        },
        "door_locked": {
            "block_mov": True,
            "block_sight": True,
            "id": ord("="),
            "color": (161, 161, 161)
        },
        "door_open": {
            "id": 92,  # ord("\\")
            "color": (161, 161, 161)
        },
        "water": {
            "id": ord("="),
            "color": GAME_COLORS["blue"]
        },

        "mountain": {
            "id": ord("A"),
            "color": GAME_COLORS["light_chartreuse"]
        },
        "hill": {
            "id": ord("n"),
            "color": GAME_COLORS["dark_chartreuse"]
        },
        "land": {
            "id": ord("."),
            "color": GAME_COLORS["darker_green"]
        },
        "coast": {
            "id": ord("´"),
            "color": GAME_COLORS["darker_amber"]
        },
        "shallow_water": {
            "id": ord("~"),
            "color": GAME_COLORS["dark_blue"]
        },
        "deep_water": {
            "id": ord("¬"),
            "color": GAME_COLORS["darkest_blue"]
        }
    }

    def __init__(self, pos, template, block_mov=None, block_sight=None,
                 id=None, color=None, room=None):
        """..."""
        self.name = template

        component = dict(self._base)
        component.update(self.templates[template])

        component["block_mov"] = block_mov or component["block_mov"]
        component["block_sight"] = block_sight or component["block_sight"]
        component["id"] = id or component["id"]
        component["color"] = color or component["color"]

        for key, value in component.items():
            setattr(self, key, value)

        self.room = room
        self.visible = False
        self.explored = False
        self.tiling_index = 0
        self.tile_variation = 0
        self.max_var = 0

        x, y = pos
        self.rect = Rect(x, y, TILE_W, TILE_H)

    @property
    def pos(self):
        """..."""
        return Position((self.rect.x, self.rect.y))

    @property
    def x(self):
        """..."""
        return self.rect.x

    @property
    def y(self):
        """..."""
        return self.rect.y

    @property
    def left(self):
        """..."""
        return self.rect.left

    @property
    def right(self):
        """..."""
        return self.rect.right

    @property
    def top(self):
        """..."""
        return self.rect.top

    @property
    def bottom(self):
        """..."""
        return self.rect.bottom

    def __floordiv__(self, n):
        """..."""
        try:
            return Position(int(self.x // n[0]), int(self.y // n[1]))
        except TypeError:
            return Position(int(self.x // n), int(self.y // n))
