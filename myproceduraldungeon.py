"""Dungeon generator.

- split the grid of 66x66 in 5-9 rows and 5-9 cols of
SECTOR_SIZExSECTOR_SIZE sections;
- for each section:
    > define room size:
        w= rnd(min_size, max_size)
        h= rnd(min_size, max_size)
    > define NW corner:
        x = rnd(section.x0, section.x1 - w)
        y = rnd(section.y0, section.y1 - h)
    > validate room;
    > place room if valid.
- pick a random room and define it as start and place up stairs.
- choose an unconnected random room and try to connect to it by digging a
hall that do not overlaps or touches other rooms (a* pathfinding). Use reduced
movement cost for hall tiles (to avoid redundant halls).
- repeat previous step until all are connected.
- make the last room used as end and place down stairs.
"""


import random
import math

from map_gen import rnd_gen
from tile import Tile
from gamemap import reg_convex_poly_room

from constants import ROOM_MIN_SIZE, ROOM_MAX_SIZE

import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

SECTOR_SIZE = 16


class SectorRect(rnd_gen.RoomRect):
    """..."""


class RoomRect(rnd_gen.RoomRect):
    """..."""


class RndMap(rnd_gen.RndMap):
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
        for x in range(sectors_wide):
            for y in range(sectors_high):
                self.sectors[(x, y)] = SectorRect(
                    x=x * SECTOR_SIZE, y=y * SECTOR_SIZE,
                    w=SECTOR_SIZE, h=SECTOR_SIZE)

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
                        self.map[pos] = Tile(pos, 'floor')
            else:
                for x in range(room.x1, room.x2 + 1):
                    for y in range(room.y1, room.y2 + 1):
                        self.map[x, y] = Tile((x, y), 'floor')

        self.map[start.random_point(self.map)].id = ord("<")
        self.map[end.random_point(self.map)].id = ord(">")

        return start, end

    def print(self):
        """..."""
        for y in range(self.height):
            for x in range(self.width):
                print(chr(self.map[(x, y)].id), end="")
            print()

    def create_halls(self):
        """..."""
        def dig_hall(target):
            path = a_star_search(self.map,
                                 target.center, room.center,
                                 self.width, self.height)

            # print("Path from start to end", path)
            for pos in path:
                if self.map[pos].id == ord("#"):
                    self.map[pos].id = ord("/")

            return path

        def pick_a_room(who, ignore):
            room = random.choice(self.rooms)
            while room == who or room == ignore:
                room = random.choice(self.rooms)
            return room

        previous = self.start
        for room in self.rooms[1:]:
            self.halls.append(dig_hall(target=previous))
            if not random.randrange(5):
                # dig an extra hall
                print("extra")
                self.halls.append(dig_hall(target=pick_a_room(room, previous)))

            previous = room

        [setattr(self.map[pos], "id", ord("."))
            for hall in self.halls
            for pos in hall
            if self.map[pos].id == ord("/")]

    def make_map(self, *args, **kwargs):
        """..."""
        self.width, self.height = self.create_sectors()
        # fill the map with walls
        self.map = {}
        for y in range(self.height):
            for x in range(self.width):
                self.map[x, y] = Tile((x, y), 'wall')

        self.start, self.end = self.create_rooms()

        for y in range(self.height):
            for x in range(self.width):
                self.map[x, y].neighbors_4d = set()
                self.map[x, y].neighbors_8d = set()
                for i, j in [
                    (x, y - 1),  # up
                    (x + 1, y),  # right
                    (x, y + 1),  # down
                    (x - 1, y),  # left
                ]:
                    if ((0 < i < self.width) and(0 < j < self.height)):
                        self.map[x, y].neighbors_4d.add((i, j))
                for i in [x - 1, x, x + 1]:
                    for j in [y - 1, y, y + 1]:
                        if ((0 < i < self.width) and(0 < j < self.height)):
                            self.map[x, y].neighbors_8d.add((i, j))

        self.create_halls()

        return self.map, self.rooms, self.halls


def heuristic(a, b):
    """..."""
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(grid, start, goal, width, height):
    """..."""
    def cost(node):
        s = 0
        x, y = node

        for d in grid[node].neighbors_8d:
            if d in grid[node].neighbors_4d:
                if grid[d].id == ord('#'):
                    s -= 2
            elif grid[d].id != ord('#'):
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
    m = RndMap()
    m.make_map()

    img_preview(m)

    """
    from game import Game
    from constants import LIMIT_FPS, SCREEN_WIDTH, SCREEN_HEIGHT

    import test_maps

    Game(
        scene=test_maps.MapTest, framerate=LIMIT_FPS,
        width=SCREEN_WIDTH, height=SCREEN_HEIGHT,
        grid=m.map, map_cols=m.width, map_rows=m.height)
    """
