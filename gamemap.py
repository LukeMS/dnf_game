"""..."""

import math
import random

from constants import FOV_RADIUS, SCREEN_ROWS, SCREEN_COLS


class MapMgr:
    """Handles data operations with maps."""

    def __init__(self, scene):
        """..."""
        self._scene = scene

    @property
    def grid(self):
        """..."""
        return self._scene.grid

    @property
    def rooms(self):
        """..."""
        return self._scene.rooms

    @property
    def halls(self):
        """..."""
        return self._scene.halls

    @property
    def level(self):
        """..."""
        return self._scene.current_level

    @property
    def player(self):
        """..."""
        return self._scene.player

    @player.setter
    def player(self, value):
        """..."""
        self._scene.player = value

    def get_cell_at_pos(self, pos):
        """..."""
        return self.grid[pos]

    def get_area(self, pos, radius):
        """..."""
        return Area.get(self.grid, pos, radius, self.width, self.height)

def get_octant(pos, distance, octant=0):
    """..."""
    def op(x, y, c, r):
        if octant == 0:
            return (x + c, y - r)
        elif octant == 1:
            return (x + r, y - c)
        elif octant == 2:
            return (x + r, y + c)
        elif octant == 3:
            return (x + c, y + r)
        elif octant == 4:
            return (x - c, y + r)
        elif octant == 5:
            return (x - r, y + c)
        elif octant == 6:
            return (x - r, y - c)
        elif octant == 7:
            return (x - c, y - r)

    octant = octant % 8

    x0, y0 = pos
    lst = []
    for row in range(1, distance):
        for col in range(0, row):
            x1, y1 = op(x0, y0, col, row)
            lst.append((x1, y1))

    return lst


def get_line(start, end):
    """Bresenham Line Algorithm.

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
