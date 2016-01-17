import random

from pygame import Rect

import tile

from constants import MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE


class RoomRect(Rect):
    # a rectangle on the map. used to characterize a room.

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def random_point(self, map, models=[tile.Floor]):
        while True:
            x = random.randint(self.x1, self.x2)
            y = random.randint(self.y1, self.y2)
            model = type(map[x, y])
            if model in models:
                break
        return x, y


class Map:
    map = {}
    rooms = []
    halls = []

    @classmethod
    def make_map(cls, width, height):
        cls.map = {}
        for y in range(height):
            for x in range(width):
                cls.map[x, y] = tile.Wall()

        num_rooms = 0
        for r in range(MAX_ROOMS):
            w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = random.randint(0, width - w - 1)
            y = random.randint(0, height - h - 1)

            new_room = RoomRect(x, y, w, h)

            failed = False
            for other_room in cls.rooms:
                if new_room.colliderect(other_room):
                    failed = True
                    break
            if not failed:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                cls.create_room(new_room)

                # center coordinates of new room, will be useful later
                new_x, new_y = new_room.center

                if num_rooms != 0:

                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    prev_x, prev_y = cls.rooms[num_rooms - 1].center

                    # draw a coin (random number that is either 0 or 1)
                    if random.randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        cls.create_h_tunnel(prev_x, new_x, prev_y)
                        cls.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        cls.create_v_tunnel(prev_y, new_y, prev_x)
                        cls.create_h_tunnel(prev_x, new_x, new_y)

                # finally, append the new room to the list
                cls.rooms.append(new_room)
                num_rooms += 1

        return dict(cls.map)

    @classmethod
    def create_room(cls, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                cls.map[x, y] = tile.Floor()
        cls.rooms.append(room)

    @classmethod
    def create_h_tunnel(cls, x1, x2, y):
        # horizontal tunnel
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        for x in range(min_x, max_x + 1):
            cls.map[x, y] = tile.Floor()
        cls.halls.append(RoomRect(min_x, y, max_x - min_x, 0))

    @classmethod
    def create_v_tunnel(cls, y1, y2, x):
        # vertical tunnel
        min_y = min(y1, y2)
        max_y = max(y1, y2) + 1
        for y in range(min_y, max_y + 1):
            cls.map[x, y] = tile.Floor()
        cls.halls.append(RoomRect(x, min_y, 0, max_y - min_y))

    @classmethod
    def rnd_open_tile(cls):
        big_list = list(cls.rooms)
        big_list.extend(cls.halls)
        place = random.choice(big_list)

        x, y = place.random_point(map=cls.map)
        return x, y
