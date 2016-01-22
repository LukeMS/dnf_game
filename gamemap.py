import math
import random


import fov
import sprite
from pathfinder import AStarSearch, GreedySearch
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
    def objects(self):
        return self._scene.objects

    @property
    def remains(self):
        return self._scene.remains

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

    def valid_tile(self, pos, goal=None):
        if goal is not None:
            if self.distance(pos, goal) > 10:
                return False

        if not (
            pos is not None and
            0 <= pos[0] < self.width
            and 0 <= pos[1] < self.height
        ):
            return False
        else:
            return not self.is_blocked(pos)[0]

    def is_blocked(self, pos, sprite=None):
        # first test the map tile
        if self.grid[pos].block_mov:
            return True, self.grid[pos]

        # now check for any blocking objects
        for object in self.objects:
            if object == sprite:
                continue
            elif object.blocks and object.pos == pos:
                return True, object

        return False, None

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

    def a_path(self, start_pos, end_pos):
        return AStarSearch.new_search(self, self.grid, start_pos, end_pos)

    def greedy_path(self, start_pos, end_pos):
        return GreedySearch.new_search(self, self.grid, start_pos, end_pos)

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
                                    x=x, y=y, group=self.remains)

                        """
                        tmp = sprite.Item(template=template, scene=self,
                                    x=x, y=y, group=self.remains)
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
                                   x=x, y=y, group=self.objects)
                if room_n == len(self.rooms) - 1:
                    pass

            elif room_n == 0:
                x, y = room.random_point(map=self.grid)
                player = getattr(self, 'player', None)
                if player:
                    self.player.pos = (x, y)
                    self.objects.add(self.player)
                    self.player.group = self.objects
                else:
                    self.player = sprite.Player(
                        scene=self._scene, x=x, y=y, group=self.objects)

                x, y = self.new_xy(room, [self.player.pos])
                template = "stair_down"
                sprite.DngFeature(template=template, scene=self._scene,
                                  x=x, y=y, group=self.remains)

                x, y = self.new_xy(room, [self.player.pos, (x, y)])

                for item in [
                    random.choice(['dagger', 'shield']),
                    'scroll of fireball'
                ]:
                    sprite.Item(template=item, scene=self._scene,
                                x=x, y=y, group=self.remains)

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
        self.grid[x, y].visible = True
        if self.distance(self.player.pos, (x, 1)) <= EXPLORE_RADIUS:
            self.grid[x, y].explored = True

    def blocks_sight(self, x, y):
        return self.grid[x, y].block_sight
