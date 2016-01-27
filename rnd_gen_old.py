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
    def __init__(self):
        self.map = {}
        self.rooms = []
        self.halls = []

    def make_map(self, width, height):
        self.map = {}
        for y in range(height):
            for x in range(width):
                self.map[x, y] = tile.Wall(pos=(x, y))

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

        return self.map, self.rooms, self.halls

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.map[x, y] = tile.Floor(pos=(x, y))
        self.rooms.append(room)

    def create_h_tunnel(self, x1, x2, y):
        # horizontal tunnel
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        for x in range(min_x, max_x + 1):
            self.map[x, y] = tile.Floor(pos=(x, y))
        self.halls.append(RoomRect(min_x, y, max_x - min_x, 0))

    def create_v_tunnel(self, y1, y2, x):
        # vertical tunnel
        min_y = min(y1, y2)
        max_y = max(y1, y2) + 1
        for y in range(min_y, max_y + 1):
            self.map[x, y] = tile.Floor(pos=(x, y))
        self.halls.append(RoomRect(x, min_y, 0, max_y - min_y))

    def rnd_open_tile(self):
        big_list = list(self.rooms)
        big_list.extend(self.halls)
        place = random.choice(big_list)

        x, y = place.random_point(map=self.map)
        return x, y