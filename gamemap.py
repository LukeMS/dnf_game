from priorityqueueset import PriorityQueueSet
import time

import sys
from game_types import Position
from random import randint

import rnd_gen
import tile

"""
    def __iter__(self):
        return iter(self.iterable)

    def __reversed__(self):
        return reversed(self.iterable)

    def __contains__(self, item):
        return item in self.iterable

    def __get_item__(self, index):
        return self.iterable[index]
"""


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
            pos.x >= 0 and pos.x < self.width and pos.y >= 0 and
            pos.y < self.height and
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

    @staticmethod
    def move_cost(pos1, pos2):
        return 1

    @staticmethod
    def manhattan(pos1, pos2):
        min_x = min(pos1.x, pos2.x)
        max_x = max(pos1.x, pos2.x)
        min_y = min(pos1.y, pos2.y)
        max_y = max(pos1.y, pos2.y)

        x_len = max_x - min_x
        y_len = max_y - min_y

        return (x_len + y_len) * 10

    def new_path(self, start_pos, end_pos):

        self.start_pos = start_pos
        self.end_pos = end_pos

        return list(self.compute_path(start_pos, end_pos))

    def compute_path(self, start, goal):
        closed_set = {}

        start_node = _Node(start)
        start_node.g_cost = 0
        start_node.f_cost = self._compute_f_cost(start_node, goal)

        open_set = PriorityQueueSet()
        open_set.add(start_node)

        while len(open_set) > 0:
            curr_node = open_set.pop_smallest()

            if curr_node.coord == goal:
                return self._reconstruct_path(curr_node)

            closed_set[curr_node] = curr_node

            for succ_coord in self.get_neighbors(curr_node.coord):
                succ_node = _Node(succ_coord)
                succ_node.g_cost = self._compute_g_cost(curr_node, succ_node)
                succ_node.f_cost = self._compute_f_cost(succ_node, goal)

                if succ_node in closed_set:
                    continue

                if open_set.add(succ_node):
                    succ_node.pred = curr_node

        return []

    def _compute_g_cost(self, from_node, to_node):
        return (from_node.g_cost +
                self.move_cost(from_node.coord, to_node.coord))

    def _compute_f_cost(self, node, goal):
        return node.g_cost + self._cost_to_goal(node, goal)

    def _cost_to_goal(self, node, goal):
        return self.manhattan(node.coord, goal)

    def _reconstruct_path(self, node):
        pth = [node.coord]
        n = node
        while n.pred:
            n = n.pred
            pth.append(n.coord)

        return reversed(pth)

    def test(self):
        t1 = time.clock()

        started, finished = None, None
        start_pos, end_pos = None, None

        while 1:
            pos = Position(
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


class _Node:
    def __init__(self, coord, g_cost=None, f_cost=None, pred=None):
        self.coord = coord
        self.g_cost = g_cost
        self.f_cost = f_cost
        self.pred = pred

    def __cmp__(self, other):
        return cmp(self.f_cost, other.f_cost)

    def __hash__(self):
        return hash(self.coord)

    def __str__(self):
        return 'N(%s) -> g: %s, f: %s' % (self.coord,
                                          self.g_cost,
                                          self.f_cost)

    def __eq__(self, other):
        return self.coord == other.coord

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def __le__(self, other):
        return self.f_cost <= other.f_cost

    def __gt__(self, other):
        return self.f_cost > other.f_cost

    def __ge__(self, other):
        return self.f_cost >= other.f_cost


if __name__ == '__main__':
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
