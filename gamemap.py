import sys
from random import randint
import queue

import rnd_gen
import tile


class Map:

    def __init__(self, width, height, objects=None):
        self.grid = rnd_gen.Map.make_map(width, height)
        self.rooms = rnd_gen.Map.rooms
        self.halls = rnd_gen.Map.halls
        self.width = width
        self.height = height

    def test(self):
        started, finished = None, None
        start_pos, end_pos = None, None

        while 1:
            pos = (randint(0, self.width - 1), randint(0, self.height - 1))
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

    def new_path(self, start_pos, end_pos):
        self.search, cost = self.a_star_search(self.grid, start_pos, end_pos)

        path = self.get_path(start_pos, end_pos)
        return path

    def get_path(self, start_pos, end_pos):
        search = self.search
        path = []
        target = tuple(end_pos)

        path = [end_pos]
        while target != start_pos:
            target = search[target]
            path.append(target)
        return path

    def get_cell_at_pos(self, pos):
        return self.grid[pos]

    def heuristic(self, start, end):
        x1, y1 = start
        x2, y2 = end
        return abs(x1 - x2) + abs(y1 - y2)

    def neighbors(self, cell):
        x, y = cell
        dirs = [(+1, 0), (0, +1), (-1, 0), (0, -1)]
        result = []
        for dir in dirs:
            neighbor = (x + dir[0], y + dir[1])
            if self.valid_tile(neighbor):
                result.append(neighbor)
        return result

    def valid_tile(self, pos):
        if pos in self.grid:
            if not self.grid[pos].block_mov:
                return True
        return False

    def a_star_search(self, graph, start, goal):
        frontier = queue.PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        cost = {}

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in self.neighbors(current):
                # new_cost = cost_so_far[current] + graph.cost(current, next))
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far


if __name__ == '__main__':
    new_map = Map(width=79, height=60)
    new_map.test()
