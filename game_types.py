"""..."""

import math
import random

from pygame import Rect
import fov

from pathfinder import AStarSearch, GreedySearch
from common import packer
from constants import TILE_W, TILE_H, GAME_COLORS


class CustomSet(set):
    """..."""

    def append(self, item):
        """Enable list method append on sets."""
        self.add(item)


class Position:
    """..."""

    # pygame.Rect

    def __init__(self, pos):
        """..."""
        self.x, self.y = pos

    @property
    def pos(self):
        """..."""
        return (self.x, self.y)

    def __mod__(self, n):
        """..."""
        try:
            return Position((self.x % n[0], self.y % n[1]))
        except TypeError:
            return Position((self.x % n, self.y % n))

    def __truediv__(self, n):
        """..."""
        try:
            return Position((self.x / n[0], self.y / n[1]))
        except TypeError:
            return Position((self.x / n, self.y / n))

    def __mul__(self, n):
        """..."""
        try:
            return Position((self.x * n[0], self.y * n[1]))
        except TypeError:
            return Position((self.x * n, self.y * n))

    def __floordiv__(self, n):
        """..."""
        try:
            return Position((self.x // n[0], self.y // n[1]))
        except TypeError:
            return Position((self.x // n, self.y // n))

    def __add__(self, n):
        """..."""
        if n:
            try:
                return Position((self.x + n[0], self.y + n[1]))
            except TypeError:
                return Position((self.x + n, self.y + n))
    """
    def __add__(self, n):
        try:
            return Position((self.x + n[0], self.y + n[1]))
        except TypeError:
            try:
                return Position((self.x + n, self.y + n))
            except TypeError:
                if n is None:
                    return self.pos
    """

    def __sub__(self, n):
        """..."""
        try:
            return Position((self.x - n[0], self.y - n[1]))
        except TypeError:
            return Position((self.x - n, self.y - n))

    def __eq__(self, n):
        """..."""
        try:
            return (self.x, self.y) == n
        except TypeError:
            return self.x == n.x and self.y == n.y

    def __iter__(self):
        """..."""
        return iter((self.x, self.y))

    def __hash__(self):
        """..."""
        return hash((self.x, self.y))

    def __repr__(self):
        """..."""
        return (self.__class__.__name__ +
                "(({x}, {y}))".format(x=self.x, y=self.y))

    def __str__(self):
        """..."""
        return (self.__class__.__name__ +
                "[x={x}, y={y}]".format(x=self.x, y=self.y))

    def __getitem__(self, key):
        """..."""
        return self.pos[key]


class TileFeature:
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

    def __init__(self, pos, template="wall", block_mov=None, block_sight=None,
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

    def __str__(self):
        """..."""
        return chr(self.id)


class TileGroup(object):
    """Contain all the objects on a map position."""

    def __init__(self, feature=None, objects=None, creatures=None):
        """..."""
        self.feature = feature
        self.objects = objects if objects else []
        self.creatures = creatures if creatures else []

    def set_feature(self, value):
        """..."""
        self.feature = value

    def add_objects(self, value):
        """..."""
        self.objects.append(value)

    def add_creatures(self, value):
        """..."""
        self.creatures.append(value)

    def remove_objects(self, value):
        """..."""
        self.objects.remove(value)

    def remove_creatures(self, value):
        """..."""
        self.creatures.remove(value)

    def get_by_type(self, _type):
        """..."""
        if _type.startswith('creature'):
            return self.creatures
        elif _type.startswith('object'):
            return self.objects


class MapHeader(object):
    """Hold essential information to identify each unique map.

    It is used as a hashable key for each map in MapContainer and assigned
    to each stair/entry to identify where it connects to.
    Additional meta map information is also stored here, such as map generator
    class used to create it and the map challenge rating (those are not used
    as part of the hashable key, however).
    """

    def __init__(self, *, name, level, split, cr, mode, **kwargs):
        """..."""
        self.__dict__.update({
            "name": name,
            "level": level,
            "split": split,
            "cr": cr,
            "mode": mode
        })
        self.__dict__.update(kwargs)

    def __hash__(self):
        """..."""
        return hash((self.name, self.level, self.split))


class MapContainer(object):
    """Hold the game maps of the game session.

    Acts as a interface to load/add a map and provides methods to work with
    them.
    """

    _maps = dict()

    def __init__(self):
        """..."""
        self.current = None

    def add(self, _map):
        """..."""
        h = _map.header
        if h not in self:
            self.store(_map)
        else:
            raise NotImplementedError

    def set_current(self, header):
        """..."""
        if self.current:
            self.store(self.current)
        self.current = self.get(header)

    def get(self, header):
        """..."""
        return packer.zshelf_unpack(self._maps[header])

    def backup(self):
        """..."""
        self.store(self.current)

    def store(self, _map):
        """..."""
        h = _map.header
        self._maps[h] = packer.zshelf_pack(_map)

    def __bool__(self):
        """Boolean state of MapContainer instances.

        return false when self.maps empty, true otherwise.
        """
        return bool(self.maps)

    def __contains__(self, item):
        """..."""
        return item in self._maps


class Map(object):
    """Each map represents a game map/level."""

    def __init__(self, *, header, cols, rows, grid=None, tile="wall"):
        """..."""
        self.header = header
        self._rooms = CustomSet()
        self._halls = CustomSet()
        self.doors = dict()
        self.cols = cols
        self.rows = rows
        self.tile_fx = list()
        self._start = None
        if not grid:
            self.grid = {(x, y): TileGroup(feature=TileFeature((x, y), tile))
                         for x in range(cols) for y in range(rows)}
        else:
            self.grid = grid
            for item in grid.values():
                assert(isinstance(item, TileGroup))

    def get_access(self, header):
        """..."""
        # TODO: implement pre-creation of headers linking on map creation.
        return self._start

    @property
    def creatures(self):
        """..."""
        for tile in self.grid.values():
            for creature in tile.creatures:
                yield creature

    @property
    def objects(self):
        """..."""
        for tile in self.grid.values():
            for obj in tile.objects:
                yield obj

    @property
    def rooms(self):
        """..."""
        return self._rooms

    @rooms.setter
    def rooms(self, value):
        self._rooms = type(self._rooms)(value)

    @property
    def halls(self):
        """..."""
        return self._halls

    @halls.setter
    def halls(self, value):
        self._halls = type(self._halls)(value)

    def items(self):
        """Act as a interface for grid attribute items."""
        return self.grid.items()

    def keys(self):
        """Act as a interface for grid attribute keys."""
        return self.grid.keys()

    def values(self):
        """Act as a interface for grid attribute values."""
        return self.grid.values()

    def has_same_id(self, t1, t2, default=False):
        """Compare the id value of two cells.

        t1 = (x1, y1) # a tuple of coordinates
        t2 = (x2, y2)
        """
        try:
            status = (self.grid[t1].feature.id ==
                      self.grid[t2].feature.id)
        except AttributeError as e:
            print(self.grid[t1])
            print(self.grid[t2])
            raise e
        return status

    def set_tile_variation(self, check_func, pos=None):
        """..."""
        if pos is None:
            for x, y in self.grid.keys():
                cell = self.grid[x, y].feature
                cell.max_var = check_func(cell.id)
                # TODO: use perlin noise instead of rnd
                if cell.max_var:
                    cell.tile_variation = random.randrange(0, cell.max_var)

    def set_tiling_index(self, pos=None):
        """..."""
        if pos is None:
            for x, y in self.grid.keys():
                self.grid[x, y].tiling_index = self.get_tiling_index(x, y)

    def get_tiling_index(self, x, y):
        """Calculate the tile index based on its neighbours."""
        s = 0
        max_x = self.cols - 1
        max_y = self.rows - 1

        # isAboveSame
        if (y - 1 < 0) or self.has_same_id((x, y), (x, y - 1)):
            s += 1

        # isLeftSame
        if (x - 1 < 0) or self.has_same_id((x, y), (x - 1, y)):
            s += 2

        # isBelowSame
        if (y + 1 >= max_y) or self.has_same_id((x, y), (x, y + 1)):
            s += 4

        # isRightSame
        if (x + 1 > max_x) or self.has_same_id((x, y), (x + 1, y)):
            s += 8

        return s

    @staticmethod
    def distance(pos1, pos2):
        """..."""
        if isinstance(pos1, tuple):
            x1, y1 = pos1
        else:
            x1, y1 = pos1.x, pos1.y

        if isinstance(pos2, tuple):
            x2, y2 = pos2
        else:
            x2, y2 = pos2.x, pos2.y

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        min_d = min(dx, dy)
        max_d = max(dx, dy)

        diagonal_steps = min_d
        straight_steps = max_d - min_d

        return math.sqrt(2) * (diagonal_steps + straight_steps)

    @staticmethod
    def heuristic(a, b):
        """..."""
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def is_blocked(self, pos, sprite=None):
        """..."""
        # first test the map tile
        if self.grid[pos].feature.block_mov:
            return True

        """
        # now check for any blocking objects
        for obj in self._scene.get_all_at_pos(
                pos, _types=["creatures", "objects"]
        ):
            if obj.combat:
                return True
        """
        return False

    def is_occupied(self, pos):
        """..."""
        return True if self.grid[pos].creatures else False

    def get_neighbors(self, pos):
        """..."""
        lst = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                n = pos + (x, y)
                if self.valid_tile(n):
                    lst.append(n)
        return lst

    def valid_tile(self, pos, goal=None):
        """..."""
        """
        if goal is not None:
            if self.distance(pos, goal) > 10:
                return False
        """

        if not (pos is not None and
                0 <= pos[0] < self.cols and
                0 <= pos[1] < self.rows):
            return False
        return True
        """
        else:
            return not self.is_blocked(pos)
        """

    def get_area(self, pos, radius):
        """..."""
        def func_visit(x, y):
            area.append((x, y))

        def func_blocked(x, y):
            return self.grid[x, y].feature.block_mov

        x, y = pos
        area = []
        fov.fieldOfView(x, y, self.cols, self.rows,
                        radius, func_visit, func_blocked)
        return area

    def a_path(self, start_pos, end_pos):
        """..."""
        """TODO:
        Make variant methods (such as neighbours) work as  single methods
        with map state ("creation", "non creation") based behaviour."""
        return AStarSearch.new_search(self, self.grid, start_pos, end_pos)

    def greedy_path(self, start_pos, end_pos):
        """..."""
        return GreedySearch.new_search(self, self.grid, start_pos, end_pos)

    def __str__(self):
        """..."""
        return "\n".join(
            "".join(chr(self.grid[x, y].feature.id) for x in range(self.cols))
            for y in range(self.rows))

    def __getitem__(self, key):
        """Act as a interface for grid attribute __getitem__."""
        try:
            return self.grid.__getitem__(key)
        except KeyError as k:
            print(key, tuple(key) in self.grid)
            raise k

    def __iter__(self):
        """Act as a interface for grid attribute __iter__."""
        return self.grid.__iter__()

    def __hash__(self):
        """..."""
        return self.header.__hash__()


if __name__ == '__main__':
    pos = Position((2, 4))
    print(pos == (2, 4))
    print(pos == Position((2, 4)))
    d = {}
    d[pos] = 1
    print(pos + (1, -1))
    print(
        Position((2, 4)) != Position((2, 5)),
        Position((2, 4)) == Position((2, 5)))
    print(tuple(pos))
    path = [(2, 4), (1, 3)]
    print(pos in path)

    print(pos % 3)
    print(pos + 2)
    print(pos * 2)

    assert(Position((1, 1)) == (1, 1))
    assert((1, 1) == Position((1, 1)))

    assert(Position((1, 1)) + (1, 1) == (2, 2))
    assert(Position((1, 1)) + (1, 1) == Position((2, 2)))

    # order matters...
    # -> can only concatenate tuple (not "Position") to tuple
    # assert((1, 1) + Position((1, 1)) == (2, 2))

    assert(Position((3, 2)) - (1, 1) == (2, 1))
    assert(Position((3, 2)) - (1, 1) == Position((2, 1)))

    assert(Position((3, 2)) == eval(Position((3, 2)).__repr__()))

    print(pos + None)

    x = MapContainer()
