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
from tile import Tile
from gamemap import reg_convex_poly_room

from constants import MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE

SECTOR_SIZE = 16


class RoomRect(Rect):
    """A rectangle on the map. used to characterize a room."""

    def __init__(self, x, y, w, h):
        """..."""
        super().__init__(x, y, w, h)

    def random_point(self, _map, templates=["floor"]):
        """..."""
        while True:
            x = random.randint(self.x1, self.x2)
            y = random.randint(self.y1, self.y2)
            if _map[x, y].name in templates:
                break
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

class SectorRect(RoomRect):
    """..."""

class Map:
    """..."""

    def __init__(self):
        """..."""
        self.map = {}
        self.rooms = []
        self.halls = []

    def make_map(self, width, height):
        """..."""
        self.map = {(x, y): Tile((x, y), 'wall')
                    for x in range(width) for y in range(height)}

        num_rooms = 0
        for r in range(MAX_ROOMS):
            w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = random.randint(0, width - w - 1)
            y = random.randint(0, height - h - 1)

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

                    # center coordinates of previous room
                    prev_x, prev_y = self.rooms[num_rooms - 1].center

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

        return self.map, self.rooms, self.halls, width, height

    def create_room(self, room):
        """Go through the tiles in the rectangle and make them passable"""
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.map[x, y] = Tile((x, y), 'floor')
        self.rooms.append(room)

    def create_h_tunnel(self, x1, x2, y):
        """Create a horizontal tunnel."""
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        for x in range(min_x, max_x + 1):
            self.map[x, y] = Tile((x, y), 'floor')
        self.halls.append(RoomRect(min_x, y, max_x - min_x, 0))

    def create_v_tunnel(self, y1, y2, x):
        """Create a vertical tunnel."""
        min_y = min(y1, y2)
        max_y = max(y1, y2) + 1
        for y in range(min_y, max_y + 1):
            self.map[x, y] = Tile((x, y), 'floor')
        self.halls.append(RoomRect(x, min_y, 0, max_y - min_y))

    def rnd_open_tile(self):
        """..."""
        big_list = list(self.rooms)
        big_list.extend(self.halls)
        place = random.choice(big_list)

        x, y = place.random_point(map=self.map)
        return x, y

class RndMap(Map):
    """..."""

    def __init__(self):
        """..."""
        self.map = {}
        self.sectors = {}
        self.rooms = []
        self.halls = []

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
            dist = heuristic((start.center), (room.center))
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
                        _map[pos] = Tile(pos, 'floor')
            else:
                [_map.__setitem__((x, y), Tile((x, y), 'floor'))
                 for x in range(room.x1, room.x2 + 1)
                 for y in range(room.y1, room.y2 + 1)]

        # _map[start.random_point(_map)].id = ord("<")
        # _map[end.random_point(_map)].id = ord(">")

        return start, end

    def print(self):
        """..."""
        _map = self.map
        h = self.height
        w = self.width

        for y in range(h):
            for x in range(w):
                print(chr(_map[(x, y)].id), end="")
            print()

    def create_halls(self):
        """..."""
        def dig_hall(target):
            # 47 == ord("/")
            # 35 == ord("#")

            path = a_star_search(_map,
                                 target.center, room.center,
                                 w, h)

            [_map[pos].__setattr__('id', 47)
             for pos in path if _map[pos].id == 35]

            return path

        def pick_a_room(who, ignore):
            rooms = self.rooms
            random.shuffle(rooms)

            for room in rooms:
                if room != who and room == ignore:
                    return room

        _map = self.map
        halls = self.halls
        rooms = self.rooms
        w = self.width
        h = self.height

        previous = self.start

        for room in rooms[1:]:
            halls.append(dig_hall(target=previous))
            if not random.randrange(5):
                # dig an extra hall
                print("extra")
                halls.append(dig_hall(target=pick_a_room(room, previous)))

            previous = room

        [_map.__setitem__(pos, Tile(pos, 'floor'))
         for hall in halls
         for pos in hall
         if _map[pos].id != ord("#")]

    def make_map(self, *args, **kwargs):
        """..."""
        w, h = self.width, self.height = self.create_sectors()
        # fill the map with walls
        self.map = {(x, y): Tile((x, y), 'wall')
                    for x in range(w) for y in range(h)}

        self.start, self.end = self.create_rooms()

        _map = self.map

        for (x, y), pos in _map.items():

            pos.neighbors_4d = {
                (i, j) for i, j in [
                    (x, y - 1),  # up
                    (x + 1, y),  # right
                    (x, y + 1),  # down
                    (x - 1, y)]  # left
                if ((0 < i < w) and (0 < j < h))}

            pos.neighbors_8d = {
                (i, j)
                for i in [x - 1, x, x + 1]
                for j in [y - 1, y, y + 1]
                if ((0 < i < w) and (0 < j < h))}

        self.create_halls()

        return _map, self.rooms, self.halls, w, h

    def __enter__(self):
        """..."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """..."""
        del self


def heuristic(a, b):
    """..."""
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(grid, start, goal, width, height):
    """..."""
    def cost(node):
        s = 0

        # ord('#') == 35

        neighbors_4d = grid[node].neighbors_4d

        for d in grid[node].neighbors_8d:
            if d in neighbors_4d:
                if grid[d].id == 35:
                    s -= 2
            elif grid[d].id != 35:
                s += 6

        return max(tile_cost[grid[node].id] + s, 0)

    def reconstruct_path(came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    tile_cost = {
        ord('/'): 0.8,
        ord('#'): 18,
        ord('.'): 32,
        ord('<'): 48,
        ord('>'): 48
    }

    start = tuple(start)
    goal = tuple(goal)

    # set boundaries
    m = 5  # margin
    min_x = max(min(grid[start].left - m, grid[goal].left - m), 1)
    min_y = max(min(grid[start].top - m, grid[goal].top - m), 1)
    max_x = min(max(grid[start].right + m, grid[goal].right + m), width - 2)
    max_y = min(max(grid[start].bottom + m, grid[goal].bottom + m), height - 2)

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
                new_cost = cost_so_far[current] + cost(next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
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
    m = {k: table[v.id] for k, v in m.map.items()}

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
    import random_seed
    random = random_seed.get_seeded(__file__)
    m = RndMap()
    m.make_map()
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

    img_preview(m)
