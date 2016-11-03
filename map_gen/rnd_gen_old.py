
class RndMap1(MapCreatorBase):
    """..."""

    def make_map(self, *, cols=MAP_COLS, rows=MAP_ROWS, **kwargs):
        """..."""
        super().make_map(cols=cols, rows=rows)

        num_rooms = 0
        new_room = None
        rooms = self.rooms
        create_room = self.create_room
        create_h_tunnel = self.create_h_tunnel
        create_v_tunnel = self.create_v_tunnel

        for r in range(MAX_ROOMS):
            w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
            x = random.randint(0, cols - w - 1)
            y = random.randint(0, rows - h - 1)

            # center coordinates of previous room
            prev_x, prev_y = new_room.center if new_room else (None, None)

            new_room = RoomRect(x, y, w, h)

            failed = False
            for other_room in rooms:
                if new_room.colliderect(other_room):
                    failed = True
                    break
            if not failed:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                create_room(new_room)

                # center coordinates of new room, will be useful later
                new_x, new_y = new_room.center

                if num_rooms != 0:

                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # draw a coin (random number that is either 0 or 1)
                    if random.randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        create_h_tunnel(prev_x, new_x, prev_y)
                        create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        create_v_tunnel(prev_y, new_y, prev_x)
                        create_h_tunnel(prev_x, new_x, new_y)

                # finally, append the new room to the list
                rooms.append(new_room)
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
