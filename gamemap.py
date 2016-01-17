import sys

from random import randint

import rnd_gen
import tile

from pathfinder import AStarSearch


class Map:
    def __init__(self, width, height, objects=None):
        self.grid, self.rooms, self.halls = rnd_gen.Map().make_map(
            width, height)
        self.width = width
        self.height = height
        self._objects = objects

    def get_cell_at_pos(self, pos):
        return self.grid[pos]

    @property
    def objects(self):
        if self._objects is None:
            return []
        else:
            return self._objects

    def valid_tile(self, pos):
        for obj in self.objects:
            if obj.pos == pos and obj.blocks:
                return False
        return (
            0 <= pos[0] < self.width and
            0 <= pos[1] < self.height and
            not self.get_cell_at_pos(pos).block_mov)

    def get_neighbors(self, pos):
        lst = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                n = pos + (x, y)
                if self.valid_tile(n) or n == self.end_pos:
                    lst.append(n)
        return lst

    def new_path(self, start_pos, end_pos):
        return AStarSearch.new_search(self, self.grid, start_pos, end_pos)

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
