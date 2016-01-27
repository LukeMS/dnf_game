import time
import pygame
import random

import pathfinder

from pygame import Rect

from tile import Tile

from constants import MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE, MAP_COLS, \
MAP_ROWS

"""
(FEATURES)
- place level: stair up
    > future: place more entries randomly
- place stair: down
    > future: place more stairs at random, maybe a tunnel trough perm wall

- generic stuff...
    > standardize the existing map creation modes;
    > make them work with feature creation
    > make them playable

(OBJECTS)
- place doors
    > future: some will be secret, trapped, locked, etc.

(CREATURES)
- place monsters:
"""


class RoomRect(Rect):
    # a rectangle on the map. used to characterize a room.

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.r_connections = []
        self.h_connections = []

    def random_point(self, map, templates=["floor"]):
        while True:
            x = random.randint(self.x1, self.x2)
            y = random.randint(self.y1, self.y2)
            if map[x, y].name in templates:
                break
        return x, y

    def add_r_connection(self, room):
        self.r_connections.append(room)

    def add_h_connection(self, hall):
        self.h_connections.append(hall)

    @property
    def x1(self):
        return self.x

    @property
    def x2(self):
        return self.x + self.w

    @property
    def y1(self):
        return self.y

    @property
    def y2(self):
        return self.y + self.h

    def __hash__(self):
        return hash((self.x, self.y, self.w, self.h))

    def valid(self, width, height):
        x1 = self.x
        if not 1 <= x1 < width - 1:
            return False

        x2 = self.x + self.w
        if not 1 <= x2 < width - 1:
            return False

        y1 = self.y
        if not 1 <= y1 < height - 1:
            return False

        y2 = self.y + self.h
        if not 1 <= y2 < height - 1:
            return False

        return True


class HallWay:
    def __init__(self, point1, point2, path):
        self.pos1, self.came_from1, self.room1 = point1
        self.pos2, self.came_from2, self.room2 = point2
        self.path = path

        self.room1.add_r_connection(self.room2)
        self.room2.add_r_connection(self.room1)

        self.room1.add_h_connection(self)
        self.room2.add_h_connection(self)

    def __iter__(self):
        return iter(self.path)


class QuarterWeightedChoice:

    def __init__(self, max_rooms, w, h):
        self.weighted_sectors_dict = {}
        x_sectors = MAP_COLS // ROOM_MAX_SIZE // 2
        y_sectors = MAP_ROWS // ROOM_MAX_SIZE // 2
        for x in range(x_sectors):
            for y in range(y_sectors):
                self.weighted_sectors_dict[(x, y)] = int(max_rooms)
        self.areas = {}
        for x in range(x_sectors):
            for y in range(y_sectors):
                """
                'sector': (x, y, w, h)
                """
                self.areas[(x, y)] = (
                    x * w // x_sectors, y * h // y_sectors,
                    (x + 1) * w // x_sectors, (y + 1) * h // y_sectors)
        self.max_rooms = max_rooms
        self.lenght = len(self.weighted_sectors_dict)

    @property
    def weighted_sectors(self):
        return [
            (key, value) for key, value in
            self.weighted_sectors_dict.items()]

    def update_weight(self, key):
        self.weighted_sectors_dict[key] -= int(self.lenght * 2)
        self.weighted_sectors_dict[key] = max(
            1,
            self.weighted_sectors_dict[key])
        # print(self.weighted_sectors)

    def get_rnd(self):
        population = [
            val for val, cnt in
            self.weighted_sectors for i in
            range(cnt)]

        sector = random.choice(population)

        area = self.areas[sector]

        return area, sector


class RndMap:
    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                print(chr(self.map[x, y].id), sep="", end="")
            print()

    def make_map(self, scene, width, height):
        self.scene = scene
        level = scene.current_level
        self.width, self.height = width, height
        self.map = scene.levels[level]['grid']
        self.rooms = scene.levels[level]['rooms']
        self.halls = scene.levels[level]['halls']
        self.hall_points = []

        # first I fill the map with walls
        for y in range(height):
            for x in range(width):
                self.map[x, y] = Tile((x, y), 'wall', block_mov=False)
        self.draw()

        print("MAX_ROOMS:", MAX_ROOMS)

        quarter_choice = QuarterWeightedChoice(MAX_ROOMS, width, height)

        num_rooms = 0
        for r in range(MAX_ROOMS):
            attempts = 0
            while attempts < 12:
                area, sector = quarter_choice.get_rnd()
                color = (255, 0, 0)

                w = (
                    random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE) + 4 -
                    attempts // 3)
                w = max(ROOM_MIN_SIZE + 4, w)

                h = (
                    random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE) + 4 -
                    attempts // 3)
                h = max(ROOM_MIN_SIZE + 4, h)

                x = random.randint(
                    area[0], area[2] - w)
                y = random.randint(
                    area[1], area[3] - h)

                new_rooms = []
                v_range = [
                    ROOM_MIN_SIZE // 2,
                    ROOM_MAX_SIZE // 2,
                    ROOM_MIN_SIZE,
                    ROOM_MAX_SIZE,
                    int(ROOM_MIN_SIZE * 2),
                    int(ROOM_MAX_SIZE * 2)
                ]
                for v in v_range:
                    for vx, vy in [
                        (x, y),
                        (x, y - v),
                        (x, y + v),
                        (x - v, y),
                        (x - v, y - v),
                        (x - v, y + v),
                        (x + v, y),
                        (x + v, y - v),
                        (x + v, y + v),
                    ]:
                        room = RoomRect(vx, vy, w, h)
                        if room.valid(width, height):
                            new_rooms.append(room)

                for room in new_rooms:
                    failed = False
                    for other_room in self.rooms:
                        if room.colliderect(other_room):
                            failed = True
                            break
                    if not failed:
                        new_room = room
                        break

                attempts += 1

                if not failed:
                    self.fill_room(new_room, block_mov=True, color=color)

                    self.rooms.append(new_room)
                    num_rooms += 1
                    quarter_choice.update_weight(sector)
                    # self.draw()
                    break
        self.draw()

        print("rooms:", len(self.rooms), 'max_rooms', MAX_ROOMS)

        for i in range(len(self.rooms)):
            room = self.rooms[i]

            self.fill_room(room, "wall", block_mov=False)
            room.inflate_ip(-2, -2)
            self.fill_room(room, "floor", block_mov=True,
                           color=(255, 255, 0))

            self.create_hall_points(room)

        self.draw()

        random.shuffle(self.hall_points)
        tmp_hall_points = list(self.hall_points)
        self.hall_connections = {}
        while True:
            if not len(self.hall_points):
                break
            wall1 = self.hall_points.pop()
            try:
                while True:
                    index = random.randint(0, len(self.hall_points) - 1)
                    wall2 = self.hall_points[index]
                    if self.valid_hall(wall1, wall2):
                        self.hall_points.pop(index)
                        break
                    elif len(self.hall_points) == 1:
                        """ The only point remaining is not valid.
                        Could lead to inifite selfish room rejection
                        loop."""
                        self.hall_points.pop(index)
            except:
                while True:
                    wall2 = random.choice(tmp_hall_points)
                    if self.valid_hall(wall1, wall2):
                        break

            self.register_connection(wall1, wall2)

            try:
                path = self.scene.map_mgr.a_path(
                    wall1[0], wall2[0], diagonals=False, check_obj=False,
                    max_distance=None)
            except KeyError as e:
                self.fill_list(
                    [wall1[0], wall2[0]], "floor", color=(123, 123, 196))
                # self.draw()
                print(e)
                continue

            hall = HallWay(
                point1=wall1,
                point2=wall2, path=path)

            self.halls.append(hall)

            self.fill_list(
                hall, "floor", color=(123, 123, 196))

            self.draw()

        tmp_hall_points = []

        self.validate_room_connection()

        for i in range(len(self.rooms)):
            room = self.rooms[i]

            self.fill_room(room, "wall", block_mov=False)
            room.inflate_ip(-2, -2)
            self.fill_room(room, "floor", block_mov=True,
                           color=(255, 255, 0))

        """
        #####################
        All done. Set walls to block_move, floors to not, etc.
        """

        # fill the map
        for y in range(height):
            for x in range(width):
                if (
                    (x == 0 or x == width - 1) or
                    (y == 0 or y == height - 1)
                ):
                    # diggable = False
                    self.map[x, y] = Tile(
                        (x, y), 'wall', color=(63, 63, 63))
                else:
                    self.map[x, y] = Tile(
                        (x, y), 'wall')

        # draw the rooms
        for room in self.rooms:
            self.fill_room(
                room, "floor")

        # draw the halls
        for hall in self.halls:
            self.fill_list(
                hall, "floor", color=(0, 0, 255))

        self.draw()

        return self.map, self.rooms, self.halls

    def register_connection(self, wall1, wall2):
        connections = self.hall_connections
        if not wall1[0] in connections:
            connections[wall1[0]] = []
        if not wall2[0] in connections:
            connections[wall2[0]] = []

        connections[wall1[0]].append(connections[wall2[0]])
        connections[wall2[0]].append(connections[wall1[0]])

    def valid_hall(self, wall1, wall2):
        connections = self.hall_connections

        if wall1[2] == wall2[2]:
            """a room cannot connect to itself..."""
            print("selfish room:", wall1[2], wall2[2])
            return False
        else:
            try:
                """two points cannot connect to each other more then
                once, that would be a waste of a (loop) hall"""
                if (
                    wall2[0] in connections[wall1[0]] or
                    wall1[0] in connections[wall2[0]]
                ):
                    print("hall loop:", wall1[2], wall2[2])
                    return False
            except KeyError:
                """no connections from this point yet"""
                return True

        return True

    def create_hall_points(self, room):
        # print(room)
        # print(self.width // 2, self.height // 2)

        weighted_choices = [
            ('top', max(1, (room.top - self.height // 2) // 5)),
            ('left', max(1, (room.left - self.width // 2) // 5)),
            ('bottom', max(1, (self.height // 2 - room.bottom) // 5)),
            ('right', max(1, (self.width // 2 - room.right) // 5))
        ]

        population = [val for val, cnt in weighted_choices for i in range(cnt)]

        rnd_time = random.randint(0, 9)

        if rnd_time < 6:
            times = 1
        elif rnd_time < 9:
            times = 2
        else:
            times = 3

        previous_choices = []
        for t in range(times):
            while True:
                came_from = random.choice(population)
                if came_from not in previous_choices:
                    previous_choices.append(came_from)
                    break

            if came_from == 'top':
                wall = (room.centerx + random.randint(-1, 1), room.top)
            elif came_from == 'right':
                wall = (room.right, room.centery + random.randint(-1, 1))
            elif came_from == 'bottom':
                wall = (room.centerx + random.randint(-1, 1), room.bottom)
            elif came_from == 'left':
                wall = (room.left, room.centery + random.randint(-1, 1))

            self.map[wall] = Tile(
                wall, "floor", block_mov=False,
                id=ord("!"), color=(0, 255, 0))
            self.hall_points.append((wall, came_from, room))

            # Hall((wall, came_from))

    def fill_room(self, room, template="floor", **kwargs):
        for x in range(room.left, room.right + 1):
            for y in range(room.top, room.bottom + 1):
                self.map[x, y] = Tile((x, y), template, **kwargs)

    def fill_list(self, _list, template="floor", **kwargs):
        for item in _list:
            self.map[item] = Tile(item, template, **kwargs)

    def rnd_open_tile(self):
        big_list = list(self.rooms)
        big_list.extend(self.halls)
        place = random.choice(big_list)

        x, y = place.random_point(map=self.map)
        return x, y

    def validate_room_connection(self):
        def visit(v_room):
            if v_room not in visited:
                visited.append(v_room)
                for n_room in v_room.r_connections:
                    visit(n_room)

        def create_connection(room_a, room_b):
            hall_a = room_a.h_connections[0]
            if hall_a.room1 == room_a:  # found itself!
                wall1 = hall_a.pos1, hall_a.came_from1, hall_a.room1
            else:
                wall1 = hall_a.pos2, hall_a.came_from2, hall_a.room2

            hall_b = room_b.h_connections[0]
            if hall_b.room1 == room_b:  # found itself!
                wall2 = hall_b.pos1, hall_b.came_from1, hall_b.room1
            else:
                wall2 = hall_b.pos2, hall_b.came_from2, hall_b.room2

            self.register_connection(wall1, wall2)
            path = self.scene.map_mgr.a_path(wall1[0], wall2[0],
                                             diagonals=False)

            hall = HallWay(point1=wall1, point2=wall2, path=path)

            self.halls.append(hall)

            self.fill_list(hall, "floor", color=(255, 255, 196))

            self.draw()

        def start():
            random.shuffle(self.rooms)
            visit(self.rooms[0])
            for room in self.rooms:
                if room not in visited:
                    print("room {} not in visited {}".format(room, visited))
                    visit(room)
                    room_a = room
                    room_b = random.choice(visited)
                    visited.remove(room_b)
                    print(room_a.__dict__)
                    create_connection(room_a, room_b)

        visited = []
        start()
        print('done?')
        # return room, visited


class River(RndMap):
    def make_map(self, scene, width, height):
        self.scene = scene
        level = scene.current_level
        self.width, self.height = width, height
        self.map = scene.levels[level]['grid']
        self.rooms = scene.levels[level]['rooms']
        self.halls = scene.levels[level]['halls']
        self.hall_points = []

        self.create_noise_map()

        for y in range(height):
            for x in range(width):
                self.map[x, y] = Tile(
                    (x, y), 'floor',
                    color=(
                        0,
                        (255 + self.noise_map[x, y]) // 2,
                        0
                    ))

        self.draw()

        self.create_river()

        self.draw()

        import resources

        print(len(resources.Tileset.cache.keys()))

        window = pygame.display.get_surface()
        pygame.image.save(window, "screenshot.jpeg")

    def create_river(self):
        pos1, pos2 = self.river_points()

        path = pathfinder.AStarSearch.new_search(
            map_mgr=self.scene.map_mgr,
            grid=self.map,
            start_pos=pos1,
            end_pos=pos2,
            cost_func=self.cost,)

        hall = HallWay(
            point1=(pos1, 0, 0),
            point2=(pos2, 0, 0), path=path)

        self.halls.append(hall)

        for _tile in hall:
            self.map[_tile] = Tile(
                _tile, "water",
                color=(
                    63,
                    63,
                    (255 + self.noise_map[_tile]) // 2
                ))

        self.enlager_river(path)

    def enlager_river(self, river):
        def add_valid_tile(n, depth_check=True):
            if (
                n not in river and
                n not in new_river_tiles
            ):
                if depth_check and self.noise_map[n] < 128:
                    new_river_tiles.append(n)
                    fill(n)
                elif not depth_check:
                    new_river_tiles.append(n)
                    fill(n)

        def fill(pos):
            self.map[pos] = Tile(
                pos, "water", color=(
                    63,
                    63,
                    (255 + self.noise_map[pos]) // 2)
            )

        new_river_tiles = []
        for _tile in river:
            for neighbor in pathfinder.AStarSearch.neighbors(
                _tile, diagonals=True
            ):
                for n_neighbor in pathfinder.AStarSearch.neighbors(
                    neighbor, diagonals=True
                ):
                    add_valid_tile(n_neighbor)
                add_valid_tile(neighbor, depth_check=False)
            self.draw()

    def river_points(self):
        points = [
            (random.randint(0, self.width - 1), 0),  # top
            (random.randint(0, self.width - 1), self.height - 1),  # bottom
            (0, random.randint(0, self.height - 1)),  # left
            (self.width - 1, random.randint(0, self.height - 1))  # right
        ]
        i = random.randint(0, len(points) - 1)
        point1 = points.pop(i)

        i = random.randint(0, len(points) - 1)
        point2 = points.pop(i)
        return point1, point2

    def cost(self, node, current):
        return self.noise_map[node]

    def create_noise_map(self):

        import noise
        noise = noise.SimplexNoise()
        self.noise_map = {}
        for y in range(self.height):
            for x in range(self.width):
                self.noise_map[x, y] = noise.get_scale_rgb(x, y)

if __name__ == '__main__':
    color = (255, 121, 122)
    color = tuple(c // 16 * 16 for c in (color))
    print(color)
