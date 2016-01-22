import sys
import math

from random import randint

import rnd_gen
import tile

from pathfinder import AStarSearch, GreedySearch


class Map:
    def __init__(self, width, height, objects=None, level=0):
        self.grid, self.rooms, self.halls = rnd_gen.Map().make_map(
            width, height)
        self.width = width
        self.height = height
        self._objects = objects
        self.level = level

    def get_cell_at_pos(self, pos):
        return self.grid[pos]

    @property
    def objects(self):
        if self._objects is None:
            return []
        else:
            return self._objects

    def valid_tile(self, pos, goal=None):
        if goal is not None:
            if self.distance(pos, goal) > 10:
                return False

        if not (
            pos is not None and
            not self.grid[pos].block_mov and
            0 <= pos[0] < self.width
            and 0 <= pos[1] < self.height
        ):
            return False
        else:
            for obj in self.objects:
                if obj.pos == pos and obj.blocks:
                    return False
            return True

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

    def get_area(self, pos, radius, circle=True, only_visible=True):
        area = []
        # print("pos {}, radius {}".format(pos, radius))
        for x in range(
            max(pos.x - radius, 0),
            min(pos.x + radius + 1, self.width)
        ):
            for y in range(
                max(pos.y - radius, 0),
                min(pos.y + radius + 1, self.height)
            ):
                # print((x, y))
                if circle and self.distance(pos, (x, y)) > radius:
                    # print((x, y), " distance:", self.distance(pos, (x, y)))
                    continue
                if only_visible and not self.grid[(x, y)].visible:
                    # print((x, y), "not visible")
                    continue
                else:
                    area.append((x, y))
        # print(area)
        return area

    def a_path(self, start_pos, end_pos):
        return AStarSearch.new_search(self, self.grid, start_pos, end_pos)

    def greedy_path(self, start_pos, end_pos):
        return GreedySearch.new_search(self, self.grid, start_pos, end_pos)

    def test(self):
        t1 = time.clock()

        started, finished = None, None
        start_pos, end_pos = None, None

        while 1:
            pos = (
                randint(0, self.width - 1), randint(0, self.height - 1))
            if started is None:
                if isinstance(
                    self.get_cell_at_pos(pos),
                    tile.Floor
                ):
                    start_pos = pos
                    started = 1
            elif finished is None:
                if isinstance(
                    self.get_cell_at_pos(pos),
                    tile.Floor
                ):
                    end_pos = pos
                    finished = 1
            else:
                break

        path = self.new_path(start_pos, end_pos)
        if True:
            print('\n', end=' ')

            for x in range(self.width):
                for y in range(self.height):
                    if (x, y) == start_pos:
                        sys.stdout.write('0')
                    elif (x, y) == end_pos:
                        sys.stdout.write('1')
                    elif (x, y) in path:
                        sys.stdout.write('~')
                    else:
                        if isinstance(
                            self.get_cell_at_pos((x, y)),
                            tile.Floor
                        ):
                            sys.stdout.write('.')
                        elif isinstance(
                            self.get_cell_at_pos((x, y)),
                            tile.Wall
                        ):
                            sys.stdout.write('#')
                print('\n', end=' ')
        t2 = time.clock()
        return t2 - t1


def test1():
    import time
    tests = []
    for i in range(1):
        mymap = Map(width=79, height=60)
        tests.append(mymap.test())
    print(sum(tests))
    """
    no-printing
    tests = [
        1.5119604586616466, 1.4198273802955415, 1.1000123619063307
    ]
    """


def test2():
    import time

    def new_point():
        lists = rnd_start + rnd_end

        while True:
            pos = (randint(0, w - 1), randint(0, h - 1))
            if pos not in lists and mymap.valid_tile(pos):
                break
        return pos

    w = 80
    h = 48

    rounds = 100

    mymap = Map(width=w, height=h)

    rnd_start = []
    rnd_end = []

    for i in range(rounds):
        rnd_start.append(new_point())
        rnd_end.append(new_point())

    t1 = time.clock()
    for i in range(rounds):
        mymap.new_path(rnd_start[i], rnd_end[i])
    t2 = time.clock()
    print("Total time spent doing pathfinding {} time(s): {}".format(
        rounds, t2-t1
    ))

if __name__ == '__main__':
    test2()
