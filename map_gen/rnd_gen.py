"""Dungeon generator.

    - split the grid of in 5-9 rows and 5-9 cols of
    SECTOR_SIZExSECTOR_SIZE sectors;
    - for each sector:
        > define room size:
            w= rnd(min_size, max_size)
            h= rnd(min_size, max_size)
        > define position in sector;
    - pick a random room and define it as start and place up stairs;
    - choose an unconnected random room and try to connect to it by digging a
    hall that do not overlaps or touches other rooms (a* pathfinding). Use
    reduced movement cost for hall tiles (to avoid redundant halls);
    - consider a random chance to put an extra connection starting on the
    current room;
    - repeat previous step until rooms all are connected;
    - make the last room used as end and place down stairs.
"""

import os
import sys
import random

from pygame import Rect

if not os.path.isdir('map_gen'):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from common import PriorityQueue
from gamemap import reg_convex_poly_room
from game_types import Map, TileFeature, MapHeader

from constants import (MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE,
                       MAP_COLS, MAP_ROWS)

SECTOR_SIZE = 16


def create_map(*, header):
    """Utility method to create by mode/name."""
    # print(dir(sys.modules[__name__]))
    creator = getattr(sys.modules[__name__], header.mode)()
    creator.header = header
    _map = creator.make_map()
    return _map


class RoomRect(Rect):
    """A rectangle on the map representing a room."""

    def __init__(self, x, y, w, h):
        """..."""
        super().__init__(x, y, w, h)

    def random_point(self, _map, templates=["floor"], ignore=[]):
        """..."""
        x_range = list(range(self.x1, self.x2 + 1))
        y_range = list(range(self.y1, self.y2 + 1))
        random.shuffle(x_range)
        random.shuffle(y_range)
        for x in x_range:
            for y in y_range:
                if _map[x, y].feature.name in templates and (
                        (x, y) not in list(ignore)):
                    return x, y

    @property
    def x1(self):
        """..."""
        return self.x

    @property
    def x2(self):
        """..."""
        return self.x + self.w

    @property
    def y1(self):
        """..."""
        return self.y

    @property
    def y2(self):
        """..."""
        return self.y + self.h

    def __hash__(self):
        """..."""
        return hash((self.x, self.y, self.w, self.h))

    def valid(self, width, height):
        """..."""
        if (1 <= self.x1 < width - 1) and \
                (1 <= self.x2 < width - 1) and \
                (1 <= self.y1 < height - 1) and \
                (1 <= self.y2 < height - 1):
            return True
        else:
            return False


class RoomIrregular(RoomRect):
    """A rectangle on the map representing a room."""

    def __init__(self, tiles):
        """..."""
        self.tiles = tiles

        x = min(tile[0] for tile in self.tiles)
        w = max(tile[0] for tile in self.tiles) - x
        y = min(tile[1] for tile in self.tiles)
        h = max(tile[1] for tile in self.tiles) - y

        super().__init__(x, y, w, h)

    def random_point(self, _map, templates=["floor"]):
        """..."""
        tiles = list(self.tiles)
        random.shuffle(tiles)
        for pos in tiles:
            if _map[pos].feature.name in templates:
                return pos


class SectorRect(RoomRect):
    """..."""


class MapCreatorBase(object):
    """..."""

    @property
    def cols(self):
        """..."""
        return self.map.cols

    @property
    def rows(self):
        """..."""
        return self.map.rows

    @property
    def rooms(self):
        """..."""
        return self.map.rooms

    @property
    def halls(self):
        """..."""
        return self.map.rooms

    def make_map(self, *, cols, rows):
        """..."""
        self.map = Map(header=self.header, cols=cols, rows=rows)


class RndMap1(MapCreatorBase):
    """..."""

    def make_map(self, *, cols=MAP_COLS, rows=MAP_ROWS, **kwargs):
        """..."""
        super().make_map(cols=cols, rows=rows)

        num_rooms = 0
        new_room = None
        for r in range(MAX_ROOMS):
            w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = random.randint(0, cols - w - 1)
            y = random.randint(0, rows - h - 1)

            # center coordinates of previous room
            prev_x, prev_y = new_room.center if new_room else (None, None)

            new_room = RoomRect(x, y, w, h)

            failed = False
            for other_room in self.rooms:
                if new_room.colliderect(other_room):
                    failed = True
                    break
            if not failed:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                new_x, new_y = new_room.center

                if num_rooms != 0:

                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # draw a coin (random number that is either 0 or 1)
                    if random.randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                # finally, append the new room to the list
                self.rooms.append(new_room)
                num_rooms += 1

        return self.map

    def create_room(self, room):
        """Dig the room tiles (make them passable)."""
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.map[x, y].feature = TileFeature((x, y), 'floor')
        self.rooms.append(room)

    def create_h_tunnel(self, x1, x2, y):
        """Create a horizontal tunnel."""
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        for x in range(min_x, max_x + 1):
            self.map[x, y].feature = TileFeature((x, y), 'floor')
        self.halls.append(RoomRect(min_x, y, max_x - min_x, 0))

    def create_v_tunnel(self, y1, y2, x):
        """Create a vertical tunnel."""
        min_y = min(y1, y2)
        max_y = max(y1, y2) + 1
        for y in range(min_y, max_y + 1):
            self.map[x, y].feature = TileFeature((x, y), 'floor')
        self.halls.append(RoomRect(x, min_y, 0, max_y - min_y))

    def rnd_open_tile(self):
        """..."""
        big_list = self.halls.union(self.rooms)
        place = random.choice(big_list)

        x, y = place.random_point(map=self.map)
        return x, y


class RndMap2(MapCreatorBase):
    """..."""

    _rooms = list()
    tile_cost = {
        ord('/'): 0.8,
        ord('#'): 18,
        ord('.'): 32,
        ord('<'): 48,
        ord('>'): 48
    }

    def __init__(self, visualize=False):
        """..."""
        super().__init__()
        self.sectors = {}
        self.visualize = visualize

    @property
    def rooms(self):
        """..."""
        return self._rooms

    def make_map(self, *, cols=MAP_COLS, rows=MAP_ROWS, **kwargs):
        """..."""
        cols, rows = self.create_sectors()
        super().make_map(cols=cols, rows=rows)

        self.start, self.end = self.create_rooms()

        for (x, y), pos in self.map.items():

            pos.neighbors_4d = {
                (i, j) for i, j in [
                    (x, y - 1),  # up
                    (x + 1, y),  # right
                    (x, y + 1),  # down
                    (x - 1, y)]  # left
                if ((0 < i < cols) and (0 < j < rows))}

            pos.neighbors_8d = {
                (i, j)
                for i in [x - 1, x, x + 1]
                for j in [y - 1, y, y + 1]
                if ((0 < i < cols) and (0 < j < rows))}

        self.create_halls()

        print("Done creating.")

        self.map.rooms = self.rooms

        return self.map

    def create_sectors(self):
        """Create n SECTOR_SIZExSECTOR_SIZE sectors.

        Return the width and height of the map now defined.
        """
        sectors_wide = random.randint(4, 6)
        sectors_high = random.randint(3, 5)

        self.sectors = {
            (x, y): SectorRect(x=x * SECTOR_SIZE, y=y * SECTOR_SIZE,
                               w=SECTOR_SIZE, h=SECTOR_SIZE)
            for x in range(sectors_wide)
            for y in range(sectors_high)}

        map_width = sectors_wide * SECTOR_SIZE
        map_height = sectors_high * SECTOR_SIZE
        print("map_width {}({}), map_height {}({})".format(
            map_width, sectors_wide, map_height, sectors_high))

        # TODO: remove this test for better performance.
        self.test_sectors()

        return map_width, map_height

    def test_sectors(self):
        """..."""
        print("Testing sectors collisions...")
        sectors = dict(self.sectors)
        while len(sectors) > 0:
            sector_a = sectors.pop(random.choice(list(sectors.keys())))
            for k in sectors.keys():
                sector_b = sectors[k]
                if sector_a.colliderect(sector_b):
                    print("Error: {} collides with {}".format(
                        sector_a, sector_b))

    def create_rooms(self):
        """Create a room in each sector.

        Go through its tiles and make them passable.
        Return a random room and the width and height of the map now defined.
        """
        _map = self.map
        _irregulars = 0
        for sector in self.sectors.values():
            if not random.randrange(60) and not _irregulars:
                w = h = ROOM_MAX_SIZE
                irregular = True
                _irregulars += 1
            else:
                irregular = False
                w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
                h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)

            try:
                x = random.randrange(sector.x1 + 1, sector.x2 - w - 2)
            except ValueError as v:
                print("x1:{}, x2:{}, w:{}".format(sector.x1, sector.x2, w))
                raise v

            try:
                y = random.randrange(sector.y1 + 1, sector.y2 - h - 2)
            except ValueError as v:
                print("x1:{}, x2:{}, w:{}".format(sector.y1, sector.y2, h))
                raise v

            new_room = RoomRect(x, y, w, h)
            new_room.irregular = irregular

            new_room._sector = sector
            sector._room = new_room

            self.rooms.append(new_room)
        print(_irregulars)

        random.shuffle(self.rooms)
        start = self.rooms[0]
        end_dist = 0
        print(start, start.center)
        for room in self.rooms[1:]:
            dist = _map.heuristic((start.center), (room.center))
            if dist > end_dist:
                end = room
                end_dist = dist

        for room in self.rooms:
            if room.irregular and room != start and room != end:
                r = room.w // 2
                # sides = random.choice([6, 8])
                sides = 8
                room_tiles = reg_convex_poly_room(sides, r, 360)
                # x, y = room.center - [r, r]
                x, y = room.left, room.top

                for r_pos, tile in room_tiles.items():
                    if tile == ".":
                        pos = (r_pos[0] + x, r_pos[1] + y)
                        _map[pos].feature = TileFeature(pos, 'floor')
            else:
                [_map[x, y].set_feature(TileFeature((x, y), 'floor'))
                 for x in range(room.x1, room.x2 + 1)
                 for y in range(room.y1, room.y2 + 1)]

            if self.visualize:
                self.print()

        # _map[start.random_point(_map)].id = ord("<")
        # _map[end.random_point(_map)].id = ord(">")

        return start, end

    def create_halls(self):
        """..."""
        def dig_hall(target):
            # 47 == ord("/")
            # 35 == ord("#")

            path = a_star_search(start=target.center, goal=room.center,
                                 grid=_map, width=w, height=h,
                                 cost_func=self.cost)

            if self.visualize:
                for pos in path:
                    if _map[pos].feature.id == 35:
                        _map[pos].feature.id = 47
                self.print()
            else:
                [_map[pos].feature.__setattr__('id', 47)
                 for pos in path if _map[pos].feature.id == 35]

            return tuple(path)

        def pick_a_room(who, ignore):
            rooms = self.rooms
            random.shuffle(rooms)

            for room in rooms:
                if room != who and room == ignore:
                    return room

        _map = self.map
        halls = self.halls
        rooms = self.rooms
        w = self.cols
        h = self.rows

        previous = self.start

        for room in rooms[1:]:
            halls.append(dig_hall(target=previous))
            if not random.randrange(5):
                # dig an extra hall
                print("extra")
                halls.append(dig_hall(target=pick_a_room(room, previous)))

            previous = room

        [_map[pos].set_feature(TileFeature(pos, 'floor'))
         for hall in halls
         for pos in hall
         if _map[pos].feature.id != ord("#")]

    def cost(self, node):
        """..."""
        _map = self.map
        tile_cost = self.tile_cost
        s = 0

        # ord('#') == 35

        neighbors_4d = _map[node].neighbors_4d

        for d in _map[node].neighbors_8d:
            if d in neighbors_4d:
                if _map[d].feature.id == 35:
                    s -= 2
            elif _map[d].feature.id != 35:
                s += 6

        return max(tile_cost[_map[node].feature.id] + s, 0)

    def print(self):
        """..."""
        self.terminal.text = self.map.__str__()
        self.terminal.game.on_event()
        self.terminal.manual_update()

    def test(self):
        """..."""
        from manager import Game
        from terminal import TerminalGrid

        game = Game(scene=TerminalGrid, framerate=10,
                    width=1024, height=768, show_fps=False,
                    scene_args={
                        'map_gen': self
                    })

    def run_test(self):
        """..."""
        self.visualize = True

        print("Test ready: make_map()")
        self.make_map()
        while self.terminal.game.alive:
            self.terminal.on_event()

    def __enter__(self):
        """..."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """..."""
        del self


class RndMap2a(RndMap2):
    """..."""

    def make_map(self, *, cols=MAP_COLS, rows=MAP_ROWS, **kwargs):
        """..."""
        super().make_map()
        return self.map

    def create_halls(self):
        """..."""
        def dig_hall(target):
            # 47 == ord("/")
            # 46 == ord(".")
            # 35 == ord("#")
            # 61 == ord("=")

            path = a_star_search(start=target.center, goal=room.center,
                                 grid=_map, width=w, height=h,
                                 cost_func=self.cost)

            # if not a room, != ord(".")
            path = [pos for pos in path if _map[pos].feature.id != 46]

            # set it to hall, = ord("/")
            [_map[pos].feature.__setattr__('id', 47)
             for pos in path if _map[pos].feature.id == 35]

            if self.visualize:
                self.print()

            return tuple(path)

        def pick_a_room(who, ignore):
            rooms = self.rooms
            random.shuffle(rooms)

            for room in rooms:
                if room != who and room == ignore:
                    return room

        _map = self.map
        halls = self.halls
        rooms = self.rooms
        doors = _map.doors = dict()
        w = self.cols
        h = self.rows

        previous = self.start
        for room in rooms[1:]:
            target = previous
            hall = dig_hall(target=target)
            halls.append(hall)
            doors[hall[0]] = room
            doors[hall[-1]] = target

            if not random.randrange(5):
                # dig an extra hall
                print("extra")
                target = pick_a_room(room, previous)
                hall = dig_hall(target=target)
                halls.append(hall)
                doors[hall[0]] = room
                doors[hall[-1]] = target

            previous = room

        [_map[pos].set_feature(TileFeature(pos, 'floor'))
         for hall in halls
         for pos in hall
         if _map[pos].feature.id != ord("#")]


class AsciiMap(MapCreatorBase):
    """Create a map from a ascii table."""

    _conversion = {
        '#': 'wall',
        '.': 'floor',
    }

    def __init__(self):
        """Initialization."""
        super().__init__()

    def make_map(self, **kwargs):
        """Create a map in game-usable format.

        Parameters:
            None (ascii-maps have specific sizes)
        """
        conversion = self._conversion
        template = self._template
        rows = len(template)
        cols = len(template[0])
        super().make_map(cols=cols, rows=rows)

        """
        assert(all([len(template[i]) == cols
                    for i in range(1, len(template))]))
        """

        [self.map[x, y].set_feature(TileFeature((x, y),
                                    conversion[template[y][x]]))
         for (x, y) in self.map.keys()]

        self.create_rooms()

        return self.map

    def create_rooms(self):
        """Convert open spaces to room structures."""
        pass


class Pit(AsciiMap):
    """Small 9x9 level with 9x9 diamond room at its center."""

    _template = ["###########",
                 "#####.#####",
                 "####...####",
                 "###.....###",
                 "##.......##",
                 "#.........#",
                 "##.......##",
                 "###.....###",
                 "####...####",
                 "#####.#####",
                 "###########"]

    def create_rooms(self):
        """Convert open spaces to room structures."""
        tiles = [(x, y) for (x, y), tile in self.map.items()
                 if tile.feature.name == 'floor']
        self.rooms.append(RoomIrregular(tiles))


"""Utiilities:"""


def a_star_search(*, grid, start, goal, width, height, cost_func):
    """..."""
    def reconstruct_path(came_from, start, goal):
        current = goal
        reconstruct_path = [current]
        while current != start:
            current = came_from[current]
            reconstruct_path.append(current)
        reconstruct_path.reverse()
        return reconstruct_path

    def feature(pos):
        return grid[pos].feature

    start = tuple(start)
    goal = tuple(goal)

    # set boundaries
    m = 5  # margin
    min_x = max(min(feature(start).left - m, feature(goal).left - m), 1)
    min_y = max(min(feature(start).top - m, feature(goal).top - m), 1)
    max_x = min(max(feature(start).right + m, feature(goal).right + m),
                width - 2)
    max_y = min(max(feature(start).bottom + m, feature(goal).bottom + m),
                height - 2)

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

        for next in grid[current].neighbors_4d:
            if (min_x <= next[0] <= max_x) and (min_y <= next[1] <= max_y):
                new_cost = cost_so_far[current] + cost_func(next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + grid.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

    return reconstruct_path(came_from, start, goal)


def img_preview(m):
    """..."""
    import PIL.Image

    table = {
        ord("#"): (0, 0, 0),
        ord("."): (223, 223, 223),
        ord("<"): (0, 255, 0),
        ord(">"): (255, 0, 0)
    }
    w, h = m.width, m.height
    m = {k: table[v.feature.id] for k, v in m.map.items()}

    img = PIL.Image.new("RGB", (w, h))

    pixels = img.load()

    for x in range(w):
        for y in range(h):
            pixels[x, y] = m[x, y]

    import matplotlib.pyplot as plt
    plt.imshow(img)

    plt.axis('off')
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()

if __name__ == '__main__':
    # import random_seed
    # random = random_seed.get_seeded(__file__)

    map_header = MapHeader(name="dungeon0", level=1, split=0, cr=0,
                           mode='RndMap2a')

    if True:
        m = RndMap2()
        m.header = map_header
        m.test()

    elif False:
        m = create_map(header=map_header)
        print(m)
    exit()

    f = __file__.replace(".py", "")
    txt = "{}.txt".format(f)
    tmp = "{}.tmp".format(f)

    import cProfile
    cProfile.run('m.make_map()', tmp)

    import pstats
    stream = open(txt.format(__file__), 'w')
    p = pstats.Stats(tmp, stream=stream)

    # 'time', 'cumulative', 'ncalls'
    p.sort_stats('cumulative').print_stats()
