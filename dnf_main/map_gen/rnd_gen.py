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

import math
import os
import random
import sys

# from prof_dec import profile_decorator

WP = os.path.join(os.path.dirname(__file__), '..', '..')
if __name__ == '__main__':
    sys.path.insert(0, WP)

from dnf_main.map_containers import Map, MapHeader

from util import roundrobin, random_seed
from util.rect import Rect
from data.constants import ROOM_MIN_SIZE, ROOM_MAX_SIZE, MAP_COLS, MAP_ROWS

SECTOR_SIZE = 16


def create_map(*, header):
    """Utility method to create by mode/name."""
    # print(dir(sys.modules[__name__]))
    creator = getattr(sys.modules[__name__], header.mode)()
    creator.header = header
    _map = creator.make_map()
    return _map


def reg_convex_poly_room(sides, radius, rotation):
    """Create a room that is in the shape of a regular convex polygon.

    Use arbitrary sides, size and rotation.

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
    m = {k: table[v._feature.id] for k, v in m.map.items()}

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


class RoomRect(Rect):
    """A rectangle on the map representing a room."""

    def __init__(self, x, y, w, h):
        """..."""
        super().__init__(x, y, w, h)

    def random_point(self, _map, templates=None, ignore=None):
        """..."""
        def get_feature(pos):
            return _map.grid.__getitem__(pos)._feature
        templates = list(templates) if templates else ["floor"]
        ignore = list(ignore) if ignore else []
        tiles = list(self.tiles)
        random.shuffle(tiles)
        for pos in tiles:
            if pos not in ignore and get_feature(pos).name in templates:
                return pos

    @property
    def tiles(self):
        """..."""
        for x in range(self.left, self.right):
            for y in range(self.top, self.bottom):
                yield (x, y)

    def __hash__(self):
        """..."""
        return hash((self.x, self.y, self.w, self.h))


class RoomIrregular(RoomRect):
    """A rectangle on the map representing a room."""

    def __init__(self, tiles):
        """..."""
        self._tiles = tiles
        x = min(tile_x for (tile_x, tile_y) in tiles)
        y = min(tile_y for (tile_x, tile_y) in tiles)
        w = max(tile_x for (tile_x, tile_y) in tiles) - x
        h = max(tile_y for (tile_x, tile_y) in tiles) - y
        super().__init__(x, y, w, h)

    @property
    def tiles(self):
        """..."""
        for tile in self._tiles:
            yield tile


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


class RndMap2(MapCreatorBase):
    """..."""

    _rooms = list()

    def __init__(self, visualize=False):
        """..."""
        self.visualize = visualize
        super().__init__()
        self.sectors = {}

    @property
    def rooms(self):
        """..."""
        return self._rooms

    @property
    def sorted_rooms(self):
        """..."""
        def distance_to_origin(room):
            return self.map.heuristic((0, 0), room.center)

        return sorted(self.rooms, key=distance_to_origin)

    def make_map(self, *, cols=MAP_COLS, rows=MAP_ROWS, **kwargs):
        """..."""
        def create_neighbors():
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

        cols, rows = self.create_sectors()
        super().make_map(cols=cols, rows=rows)

        self.start, self.end = self.create_rooms()

        create_neighbors()

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
        # self.test_sectors()

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
        def get_feature(pos):
            return grid.__getitem__(pos)._feature

        def features(gen):
            for pos in gen:
                yield get_feature(pos)

        _map = self.map
        grid = _map.grid
        _irregulars = 0
        rooms = self.rooms
        for sector in self.sectors.values():
            if not random.randrange(60) and not _irregulars:
                w = h = ROOM_MAX_SIZE
                irregular = True
                _irregulars += 1
            else:
                irregular = False
                w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
                h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)

            x = random.randrange(sector.left + 1, sector.right - w - 2)
            y = random.randrange(sector.top + 1, sector.bottom - h - 2)

            new_room = RoomRect(x, y, w, h)
            new_room.irregular = irregular

            new_room._sector = sector
            sector._room = new_room

            rooms.append(new_room)
        print(_irregulars)

        random.shuffle(self.rooms)
        start = self.rooms[0]
        end_dist = 0
        # print(start, start.center)
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
                x, y = room.left, room.top
                room.__class__ = RoomIrregular
                # x, y = room.center - [r, r]

                room._tiles = [(r_pos[0] + x, r_pos[1] + y)
                               for r_pos, tile in room_tiles.items()
                               if tile == "."]

            [feature.change_feature(template='floor')
             for feature in features(room.tiles)]

            if self.visualize:
                self.print()

        return start, end

    def create_halls(self):
        """..."""
        def get_feature(pos):
            return grid.__getitem__(pos)._feature

        def features_with_positions(gen):
            for pos in gen:
                yield get_feature(pos), pos

        def features(gen):
            for pos in gen:
                yield get_feature(pos)

        def dig_hall(target):
            path = b_star_pathfinder(
                start=target.center, goal=room.center, cost_func=cost_func)

            [feature.change_feature(template='hall')
             for feature in features(path)
             if feature.name == "wall"]

            if visualize:
                self.print()

            return tuple(path)

        def split_list_around(who):
            index = sorted_rooms.index(who)
            size = len(sorted_rooms)
            l_size = size // 2
            r_size = size - l_size - 1
            left = [v for i, v in enumerate(
                reversed(sorted_rooms + sorted_rooms[:index + 1]))
                if (v != who and i <= l_size)]
            right = [v for i, v in enumerate(
                sorted_rooms[index:] + sorted_rooms)
                if (v != who and i <= r_size)]
            return left[::-1], right

        def pick_a_room(who):
            index = sorted_rooms.index(who)
            if index < 4:
                gen = enumerate(sorted_rooms[:index] +
                                sorted_rooms[index + 1:])
                size = len(sorted_rooms) - 1
            else:
                left, right = split_list_around(who)
                gen = enumerate(roundrobin(reversed(left), right))
                size = len(left) + len(right)
            for i, room in gen:
                if i <= 1 or room == who:
                    continue
                chance = random.randrange(i + size) - i * 2
                if chance <= 1:
                    return room

        _map = self.map
        grid = _map.grid
        b_star_pathfinder = _map.b_star_pathfinder
        halls = self.halls
        visualize = self.visualize
        cost_func = self.cost

        sorted_rooms = list(self.sorted_rooms)
        for i, room in enumerate(sorted_rooms):
            if i == 0:
                previous = room
                continue
            # print("hall")
            halls.append(dig_hall(target=previous))
            if not random.randrange(5):
                # dig an extra hall
                # print("extra hall")
                halls.append(dig_hall(target=pick_a_room(room)))

            previous = room

        [feature.change_feature(template='floor')
         for hall in halls
         for feature in features(hall)
         if feature.name == "hall"]

    def cost(self, node):
        """..."""
        def get_tile_cost(pos):
            return grid.__getitem__(pos)._feature._rnd_gen_cost
        _map = self.map
        grid = _map.grid
        main = get_tile_cost(node)
        # _4d = _map[node].neighbors_4d
        # _8d = _map[node].neighbors_8d.difference(_4d)
        _8d = grid.__getitem__(node).neighbors_8d
        # sum_4d = sum(get_tile_cost(pos) for pos in _4d)
        sum_8d = sum(get_tile_cost(pos) for pos in _8d)
        # result = int(main * 6 + sum_4d + sum_8d)
        return int(main * 6 + sum_8d)

    def print(self):
        """..."""
        terminal = self.terminal
        terminal.text = self.map.__str__()
        terminal.manager.on_event()
        terminal.manual_update()

    def test(self):
        """..."""
        from scene_manager import Manager
        from dnf_main.scenes.scene_terminal import TerminalGrid

        m = Manager(scene=TerminalGrid,
                    width=1024, height=768, show_fps=False,
                    scene_args={'map_gen': self}).execute()

    def run_test(self):
        """..."""
        from dnf_main.map_gen import populate_level
        self.visualize = True

        print("Test ready: make_map()")
        self.make_map()
        populate_level.populate(scene=self.terminal, _map=self.map)
        self.print()

        while self.terminal.manager.alive:
            self.terminal.on_event()

    def __enter__(self):
        """..."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """..."""
        del self


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
        template = self._template
        rows = len(template)
        cols = len(template[0])
        super().make_map(cols=cols, rows=rows)

        self.create_rooms()

        return self.map

    def create_rooms(self):
        """Convert open spaces to room structures."""
        def get_template_name(pos):
            x, y = pos
            return conversion[template[y][x]]

        conversion = self._conversion
        template = self._template
        [tile.change_feature(template='floor')
         for tile in self.map.tiles
         if tile.name == "wall" and
         get_template_name(tile.pos) == "floor"]

        tiles = [tile.pos for tile in self.map.tiles
                 if tile.name == 'floor']

        self.rooms.append(RoomIrregular(tiles))


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

if __name__ == '__main__':
    # @profile_decorator
    def main(visualize=False):
        """..."""
        if visualize:
            m = RndMap2()
            m.header = map_header
            m.test()
        else:
            m = create_map(header=map_header)
            print(m)

    random = random_seed.get_seeded(__file__)

    map_header = MapHeader(name="dungeon0", level=1, split=0, cr=0,
                           mode='RndMap2')
    main(visualize=False)
