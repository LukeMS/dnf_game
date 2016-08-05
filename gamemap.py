import math
import random


import fov
import sprite
from pathfinder import AStarSearch, GreedySearch
from rnd_utils import RoomItems, rnd_cr_per_level  # , ItemTypes, MonsterTypes
from combat.bestiary import Bestiary

from constants import MAP_COLS, MAP_ROWS, MAX_ROOM_MONSTERS
from constants import EXPLORE_RADIUS, FOV_RADIUS, SCREEN_ROWS, SCREEN_COLS


class Map:

    @classmethod
    def __init__(cls, scene):
        cls._scene = scene

    @classmethod
    def __setitem__(cls, key, value):
        dic = cls._scene.levels[cls._scene.current_level]['grid']
        dic[key]['feature'] = value

    @classmethod
    def __getitem__(cls, key):
        dic = cls._scene.levels[cls._scene.current_level]['grid']
        return dic[key]['feature']

    @classmethod
    def keys(cls):
        dic = cls._scene.levels[cls._scene.current_level]['grid']
        return dic.keys()


class MapMgr:
    """Handles data operations with maps."""

    def __init__(self, scene):
        self._scene = scene

    @property
    def grid(self):
        return self._scene.grid

    @property
    def rooms(self):
        return self._scene.rooms

    @property
    def halls(self):
        return self._scene.halls

    @property
    def level(self):
        return self._scene.current_level

    @property
    def player(self):
        return self._scene.player

    @player.setter
    def player(self, value):
        self._scene.player = value

    @property
    def width(self):
        return MAP_COLS

    @property
    def height(self):
        return MAP_ROWS

    def get_cell_at_pos(self, pos):
        return self.grid[pos]

    def get_area(self, pos, radius):
        return Area.get(self.grid, pos, radius)

    def get_neighbors(self, pos):
        lst = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                n = pos + (x, y)
                if self.valid_tile(n):
                    lst.append(n)
        return lst

    def has_same_id(self, t1, t2, invalid_return_value=True):
        """Compare the id value of two cells.

        t1 = (x1, y1) # a tuple of coordinates
        t2 = (x2, y2)
        """
        try:
            status = self.grid[t1].id == self.grid[t2].id
            return status
        except KeyError:
            return invalid_return_value

    def set_tile_variation(self, check_func, pos=None):
        if pos is None:
            for x, y in self.grid.keys():
                cell = self.grid[x, y]
                cell.max_var = check_func(cell.id)
                # TODO: use perlin noise instead of rnd
                if cell.max_var:
                    cell.tile_variation = random.randrange(0, cell.max_var)

    def set_tiling_index(self, pos=None):
        if pos is None:
            for x, y in self.grid.keys():
                self.grid[x, y].tiling_index = self.get_tiling_index(x, y)

    def get_tiling_index(self, x, y):
        """Calculate the tile index based on its neighbours."""
        s = 0
        max_x = self.width - 1
        max_y = self.height - 1

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
    def get_octant(pos, distance, octant=0):
        octant = octant % 8
        if octant == 0:
            op = lambda x, y, c, r: (x + c, y - r)
        elif octant == 1:
            op = lambda x, y, c, r: (x + r, y - c)
        elif octant == 2:
            op = lambda x, y, c, r: (x + r, y + c)
        elif octant == 3:
            op = lambda x, y, c, r: (x + c, y + r)
        elif octant == 4:
            op = lambda x, y, c, r: (x - c, y + r)
        elif octant == 5:
            op = lambda x, y, c, r: (x - r, y + c)
        elif octant == 6:
            op = lambda x, y, c, r: (x - r, y - c)
        elif octant == 7:
            op = lambda x, y, c, r: (x - c, y - r)
        x0, y0 = pos
        lst = []
        for row in range(1, distance):
            for col in range(0, row):
                x1, y1 = op(x0, y0, col, row)
                lst.append((x1, y1))

        return lst
        """
        for (var row = 1; row < maxDistance; row++) {
          for (var col = 0; col <= row; col++) {
            var x = hero.x + col;
            var y = hero.y - row;

            paint(x, y);
          }
        }
        """

    @staticmethod
    def get_line(start, end):
        """Bresenham's Line Algorithm
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

    def valid_tile(self, pos, goal=None):
        """
        if goal is not None:
            if self.distance(pos, goal) > 10:
                return False
        """

        if not (
            pos is not None and
            0 <= pos[0] < self.width
            and 0 <= pos[1] < self.height
        ):
            return False
        else:
            return not self.is_blocked(pos)

    def is_blocked(self, pos, sprite=None):
        # first test the map tile
        if self.grid[pos].block_mov:
            return True

        # now check for any blocking objects
        for obj in self._scene.get_all_at_pos(
                pos, _types=["creatures", "objects"]
        ):
            if obj.combat:
                return True

        return False

    @staticmethod
    def distance(pos1, pos2):
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

    def a_path(self, start_pos, end_pos):
        return AStarSearch.new_search(self, self.grid, start_pos, end_pos)

    def greedy_path(self, start_pos, end_pos):
        return GreedySearch.new_search(self, self.grid, start_pos, end_pos)

    def new_xy(self, room, objects=None):
        attempts = 0
        while True:
            if attempts > 10:
                return None
            xy = room.random_point(_map=self.grid)
            if xy not in objects:
                return xy
            attempts += 1

    def place_objects(self):
        # level ?
        level = self._scene.current_level
        for room_n, room in enumerate(self.rooms):

            if room_n > 2:
                num_items = RoomItems.random()
                items_placed = []
                for i in range(num_items):
                    xy = self.new_xy(room, items_placed)
                    if xy is not None:
                        items_placed.append(xy)
                        x, y = xy
                        # template = ItemTypes.random()
                        sprite.Item(template="healing potion",
                                    scene=self._scene,
                                    x=x, y=y)

                        """
                        tmp = sprite.Item(template=template, scene=self,
                                    x=x, y=y)
                        tmp.item.pick_up(getter=self.player)
                        """

                num_monsters = random.randint(0, MAX_ROOM_MONSTERS)
                monsters_placed = []
                for i in range(num_monsters):
                    xy = self.new_xy(room, monsters_placed)
                    if xy is not None:
                        monsters_placed.append(xy)
                        x, y = xy
                        # template = MonsterTypes.random()
                        template = Bestiary.get_by_cr(rnd_cr_per_level(level))
                        sprite.NPC(template=template,
                                   scene=self._scene,
                                   x=x, y=y)
                if room_n == len(self.rooms) - 1:
                    pass

            elif room_n == 0:
                x, y = room.random_point(_map=self.grid)
                player = getattr(self, 'player', None)
                if player:
                    self._scene.rem_obj(self.player, 'creatures',
                                        self.player.pos)

                    self.player.pos = (x, y)

                    self._scene.add_obj(self.player, 'creatures',
                                        self.player.pos)
                else:
                    self.player = sprite.Player(
                        scene=self._scene, x=x, y=y)

                x, y = self.new_xy(room, [self.player.pos])
                template = "stair_down"
                sprite.DngFeature(template=template, scene=self._scene,
                                  x=x, y=y)

                x, y = self.new_xy(room, [self.player.pos, (x, y)])

                for item in [
                    # random.choice(['falchion', 'aklys']),
                    'scroll of fireball', 'scroll of confusion',
                    "bastard's sting", "shortsword", "studded leather"
                ]:
                    sprite.Item(template=item, scene=self._scene,
                                x=x, y=y)

    def set_fov(self):
        self._scene.set_offset(self.player)
        for y in range(SCREEN_ROWS):
            for x in range(SCREEN_COLS):
                pos = self._scene.offset + (x, y)
                self.grid[pos].visible = False

        fov.fieldOfView(self.player.x, self.player.y,
                        MAP_COLS, MAP_ROWS, FOV_RADIUS,
                        self.func_visible, self.blocks_sight)

    def func_visible(self, x, y):
        self.grid[x, y].visible = True
        # if self.distance(self.player.pos, (x, y)) <= EXPLORE_RADIUS:
        self.grid[x, y].explored = True

    def blocks_sight(self, x, y):
        return self.grid[x, y].block_sight


class Area:

    @classmethod
    def get(cls, grid, pos, radius):
        cls.grid = grid

        x, y = pos

        cls.area = []

        fov.fieldOfView(
            x, y, MAP_COLS, MAP_ROWS,
            radius, cls.func_visit, cls.func_blocked
        )

        return cls.area

    @classmethod
    def func_visit(cls, x, y):
        cls.area.append((x, y))

    @classmethod
    def func_blocked(cls, x, y):
        return cls.grid[x, y].block_mov


def reg_convex_poly_room(sides, radius, rotation):
    """Create a room that is in the shape of a regular convex polygon with
    arbitrary sides, size and rotation.

    by Quintin Steiner - 22.10.2015
    (translated to python)

    Steps:
    Draw walls by picking pairs of points around a circle and linearly
    interpolating between them. The number of pairs should equal the number of
    sides of the shape. You will need to use trig for this.
    Create a floor by filling the shape using some sort of fill algorithm.

    You can then create a doughnut shaped room by subtracting a smaller
    generated room from the center of a larger generated room. You should keep
    the walls of the smaller generated room though.

    Source: http://www.we-edit.de/gamedev/question
    /generating-39specially39-shaped-rooms-for-a-dungeon-110089.html
    """

    # convert the rotation degrees to radians.
    rotation *= math.pi / 180.0

    # make an array size that is sure to fit the room.
    room_size = math.ceil(radius * 2) + 1

    room = {}
    for i in range(room_size):
        for j in range(room_size):
            room[i, j] = None

    # first we must create the walls of the room.
    rchange = (math.pi * 2.0) / sides

    r = 0
    while r < math.pi * 2:
        # for (double r = 0; r < Math.PI * 2; r += rchange)
        # define first point.
        p1_x = radius + math.cos(r + rotation) * radius
        p1_y = radius + math.sin(r + rotation) * radius

        # define second point (rotated 1 iteration further).
        p2_x = radius + math.cos(r + rotation + rchange) * radius
        p2_y = radius + math.sin(r + rotation + rchange) * radius

        # get distance between the two points.
        l = math.sqrt(math.pow(p2_x - p1_x, 2) + math.pow(p2_y - p1_y, 2))

        # linearly interpolate between the two points and place walls
        # between them.
        i = 0
        # for (double i = 0; i < 1; i += 1.0 / l)
        while i < 1:
            place_x = round((1 - i) * p1_x + i * p2_x)
            place_y = round((1 - i) * p1_y + i * p2_y)

            room[place_x, place_y] = '#'

            i += 1.0 / l

        r += rchange

    # now we have to fill the room with a floor.
    # this is done using something similar to a scanline algorithm.
    # for (int scan = 0; scan < roomSize; scan++)
    for scan in range(room_size):
        left_x = -1
        right_x = -1
        space_detected = False

        # for (int i = 0; i < roomSize; i++)
        for i in range(room_size):
            if (room[i, scan] == '#'):
                if not space_detected:
                    left_x = i
                else:
                    right_x = i
                    break
            elif left_x != -1:
                space_detected = True

        if (right_x != -1):
            # for (int i = left_x + 1; i < right_x; i++)
            for i in range(left_x + 1, right_x):
                room[i, scan] = '.'

    return room
