"""..."""

import random

from dnf_game.data.tiles_index import TilesetIndex
from dnf_game.dnf_main.map_entities import TileEntity
from dnf_game.util import CustomSet, PriorityQueue


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
        self.name = name
        self.level = level
        self.split = split
        self.cr = cr
        self.mode = mode
        self.__dict__.update(kwargs)

    def __hash__(self):
        """..."""
        return hash((self.name, self.level, self.split))

    def __str__(self):
        """..."""
        return self.__repr__()

    def __repr__(self):
        """..."""
        return "%s(name=%s, level=%d, split=%d)" % (
            self.__class__.__name__,
            self.name,
            self.level,
            self.split)


class MapContainer(object):
    """Hold the game maps of the game session.

    Acts as a interface to load/add a map and provides methods to work with
    them.
    """

    def __init__(self):
        """..."""
        self._maps = dict()
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
        return self._maps[header]

    def backup(self):
        """..."""
        self.store(self.current)

    def store(self, _map):
        """..."""
        h = _map.header
        self._maps[h] = _map

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
            self.grid = {(x, y): TileGroup(feature=TileEntity(
                name=tile, pos=(x, y), template=tile, scene=None))
                for x in range(cols) for y in range(rows)}
        else:
            self.grid = grid

    def get_access(self, header):
        """..."""
        # TODO: implement pre-creation of headers linking on map creation.
        return self._start

    @property
    def entities(self):
        """..."""
        for _type in (self.tiles, self.creatures, self.objects):
            for entity in _type:
                yield entity

    @property
    def tiles(self):
        """..."""
        for tile in self.grid.values():
            yield tile.feature

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

    def set_tile_variation(self, pos=None):
        """..."""
        if pos is None:
            for x, y in self.grid.keys():
                cell = self.grid[x, y].feature
                cell.max_var = TilesetIndex.get_var(cell)
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
    def get_line(start, end):
        """Bresenham Line Algorithm.

        Produces a list of tuples from start and end

        >>> points1 = get_line((0, 0), (3, 4))
        >>> points2 = get_line((3, 4), (0, 0))
        >>> assert(set(points1) == set(points2))
        >>> print points1
        [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
        >>> print points2
        [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
        """
        # Setup initial conditions
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1

        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)

        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Swap start and end points if necessary and store swap state
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True

        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1

        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        # Reverse the list if the coordinates were swapped
        if swapped:
            points.reverse()
        return points

    @staticmethod
    def get_octant(pos, distance, octant=0):
        """..."""
        def op(x, y, c, r):
            if octant == 0:
                return (x + c, y - r)
            elif octant == 1:
                return (x + r, y - c)
            elif octant == 2:
                return (x + r, y + c)
            elif octant == 3:
                return (x + c, y + r)
            elif octant == 4:
                return (x - c, y + r)
            elif octant == 5:
                return (x - r, y + c)
            elif octant == 6:
                return (x - r, y - c)
            elif octant == 7:
                return (x - c, y - r)

        octant = octant % 8

        x0, y0 = pos
        lst = []
        for row in range(1, distance):
            for col in range(0, row):
                x1, y1 = op(x0, y0, col, row)
                lst.append((x1, y1))

        return lst

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

    def blocks_sight(self, x, y):
        """..."""
        return any(item.block_sight
                   for item in self.grid[x, y].get_all()
                   if item)

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

    def cost(self, node):
        """..."""
        return 1

    def reconstruct_path(self, came_from, start, goal):
        """..."""
        current = goal
        reconstruct_path = [current]
        while current != start:
            current = came_from[current]
            reconstruct_path.append(current)
        reconstruct_path.reverse()
        return reconstruct_path

    def greedy_pathfinder(self, start, goal, mode="8d"):
        """..."""
        grid = self.grid
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        came_from[start] = None

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            neighbors = grid[current].neighbors_8d if mode == "8d" \
                else grid[current].neighbors_4d
            for next in neighbors:
                if next not in came_from:
                    priority = self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current
        return self.reconstruct_path(came_from, start, goal)

    def a_star_pathfinder(self, start, goal, mode="8d"):
        """..."""
        grid = self.grid
        frontier = PriorityQueue()
        came_from = {}
        cost_so_far = {}

        frontier.put(start, 0)
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            neighbors = grid[current].neighbors_8d if mode == "8d" \
                else grid[current].neighbors_4d
            for next in neighbors:
                new_cost = cost_so_far[current] + self.cost(next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

            if current == goal:
                break

        return self.reconstruct_path(came_from, start, goal)

    def b_star_pathfinder(self, *, start, goal, cost_func):
        """..."""
        def feature(pos):
            return grid.__getitem__(pos).feature

        def boundaries():
            _start_feat = feature(start)
            _goal_feat = feature(goal)

            left = min(_start_feat.left, _goal_feat.left)
            min_x = max(left - m, 0)

            top = min(_start_feat.top, _goal_feat.top)
            min_y = max(top - m, 0)

            right = max(_start_feat.right, _goal_feat.right)
            max_x = min(right + m, self.cols - 1)

            bottom = max(_start_feat.bottom, _goal_feat.bottom)
            max_y = min(bottom + m, self.rows - 1)

            return min_x, min_y, max_x, max_y
            return min_x, min_y, max_x, max_y

        def inside_boundaries(pos):
            return (min_x < pos[0] < max_x) and (min_y < pos[1] < max_y)

        grid = self.grid
        heuristic = self.heuristic
        reconstruct_path = self.reconstruct_path
        start = tuple(start)
        goal = tuple(goal)

        # set boundaries
        m = 5  # margin
        min_x, min_y, max_x, max_y = boundaries()

        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for nxt in grid.__getitem__(current).neighbors_4d:
                if inside_boundaries(nxt):
                    new_cost = (cost_so_far.__getitem__(current) +
                                cost_func(nxt))
                    if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                        cost_so_far.__setitem__(nxt, new_cost)
                        priority = new_cost + heuristic(goal, nxt)
                        frontier.put(nxt, priority)
                        came_from.__setitem__(nxt, current)

        return reconstruct_path(came_from, start, goal)

    def __str__(self):
        """..."""
        cols = self.cols
        rows = self.rows
        grid = self.grid

        return "\n".join(
            "".join(chr(grid.__getitem__((x, y)).feature.id)
                    for x in range(cols))
            for y in range(rows))

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


class TileGroup(object):
    """Contain all the objects on a map position."""

    def __init__(self, feature=None, objects=None, creatures=None):
        """..."""
        self._feature = feature
        self._objects = objects or []
        self._creatures = creatures or []

    @property
    def pos(self):
        """..."""
        return self.feature.pos

    @property
    def feature(self):
        """..."""
        return self._feature

    @feature.setter
    def feature(self, value):
        """..."""
        self._feature = value

    def set_feature(self, value):
        """..."""
        self.__setattr__("_feature", value)

    @property
    def objects(self):
        """..."""
        return self._objects

    @property
    def creatures(self):
        """..."""
        return self._creatures

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

    def get_all(self):
        """..."""
        return [self.feature] + self.objects + self.creatures

    def __str__(self):
        """..."""
        return ("{name}(pos:{pos}; feature:{feature}; "
                "objects:{objects}; creatures:{creatures})").format(
            name=self.__class__.__name__, pos=self.pos, feature=self.feature,
            objects=self.objects, creatures=self.creatures)
