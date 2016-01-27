import math
import random


import fov
import sprite
from pathfinder import AStarSearch
from rnd_utils import RoomItems, ItemTypes, MonsterTypes

from constants import MAP_COLS, MAP_ROWS, MAX_ROOM_MONSTERS
from constants import EXPLORE_RADIUS, FOV_RADIUS, SCREEN_ROWS, SCREEN_COLS


class Map:
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

    def valid_tile(self, pos, goal=None, check_obj=True, max_distance=10):
        """
        if max_distance and goal is not None:
            if self.distance(pos, goal) > max_distance:
                return False
        """
        if not (
            pos is not None and
            0 <= pos[0] < self.width
            and 0 <= pos[1] < self.height
        ):
            return False
        else:
            return not self.is_blocked(pos, check_obj=check_obj)

    def is_blocked(self, pos, check_obj=True):
        if self.grid[pos].block_mov:
            return True

        """
        if check_obj:

            for obj in self._scene.get_all_at_pos(
                pos, _types=["creatures", "objects"]
            ):
                if obj.fighter:
                    return True
        """

        return False

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

    def a_path(self, start_pos, end_pos,
               diagonals=True, check_obj=True, max_distance=10):
        a_star = AStarSearch(map_mgr=self, grid=self.grid)
        path = a_star.new_search(start_pos, end_pos,
                                 diagonals=diagonals, check_obj=check_obj,
                                 max_distance=max_distance)
        print("path:", path)
        return path

    def distance(self, pos1, pos2):
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

    def new_xy(self, room, objects=None):
        attempts = 0
        while True:
            if attempts > 10:
                return None
            xy = room.random_point(map=self.grid)
            if xy not in objects:
                return xy
            attempts += 1

    def place_objects(self):
        for room_n, room in enumerate(self.rooms):

            if room_n > 2:
                num_items = RoomItems.random()
                items_placed = []
                for i in range(num_items):
                    xy = self.new_xy(room, items_placed)
                    if xy is not None:
                        items_placed.append(xy)
                        x, y = xy
                        template = ItemTypes.random()
                        sprite.Item(template=template, scene=self._scene,
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
                        template = MonsterTypes.random()
                        sprite.NPC(template=template, scene=self._scene,
                                   x=x, y=y)
                if room_n == len(self.rooms) - 1:
                    pass

            elif room_n == 0:
                x, y = room.random_point(map=self.grid)
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
                    random.choice(['dagger', 'shield']),
                    'scroll of fireball'
                ]:
                    sprite.Item(template=item, scene=self._scene,
                                x=x, y=y)

    def set_fov(self):
        self._scene.set_offset(self.player)
        for y in range(SCREEN_ROWS):
            for x in range(SCREEN_COLS):
                # draw tile at (x,y)
                tile = self.grid[self._scene.offset + (x, y)]
                tile.visible = False

        fov.fieldOfView(self.player.x, self.player.y,
                        MAP_COLS, MAP_ROWS, FOV_RADIUS,
                        self.func_visible, self.blocks_sight)

    def func_visible(self, x, y):
        level_dict = self._scene.levels[self._scene.current_level]
        level_dict[x, y]['feature'].visible = True
        if self.distance(self.player.pos, (x, 1)) <= EXPLORE_RADIUS:
            level_dict[x, y]['feature'].explored = True

    def blocks_sight(self, x, y):
        level_dict = self._scene.levels[self._scene.current_level]
        return level_dict[x, y]['feature'].block_sight


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
