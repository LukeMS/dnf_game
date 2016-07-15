"""..."""

import random

from common import PriorityQueue


class PathFinders:
    """..."""

    @staticmethod
    def heuristic(a, b):
        """..."""
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def reconstruct_path(came_from, start, goal):
        """..."""
        current = goal
        reconstruct_path = [current]
        while current != start:
            current = came_from[current]
            reconstruct_path.append(current)
        reconstruct_path.reverse()
        return reconstruct_path

    @classmethod
    def valid_tile(cls, pos):
        """..."""
        if not (
            pos is not None and
            0 <= pos[0] < cls.width and
            0 <= pos[1] < cls.height
        ):
            return False
        return True

    @classmethod
    def neighbors(cls, node, goal=None):
        """..."""
        lst = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                n = (node[0] + x, node[1] + y)
                try:
                    valid = (cls.map_mgr.valid_tile(n, goal) or
                             n == goal)
                except:
                    valid = cls.valid_tile or n == goal
                if valid:
                    lst.append(n)
        return lst


class GreedySearch(PathFinders):
    """..."""

    @classmethod
    def test(cls):
        """..."""
        height = cls.height = 4
        width = cls.width = 4

        grid = ["."] * height
        for y in range(height):
            grid[y] = ["."] * width

        start = (
            random.randint(0, width - 1),
            random.randint(0, height - 1))
        while True:
            goal = (
                random.randint(0, width - 1),
                random.randint(0, height - 1))
            if goal != start:
                break

        search = cls.search(start, goal)
        path = cls.reconstruct_path(search, start, goal)

        for node in path:
            x, y = node
            grid[y][x] = "~"

        grid[start[1]][start[0]] = "@"

        grid[goal[1]][goal[0]] = "!"

        print(start, goal)
        print(path)
        for y in range(height):
            for x in range(width):
                print(grid[y][x], sep='', end='')
            print()

    @classmethod
    def new_search(cls, map_mgr, grid, start_pos, end_pos):
        """..."""
        cls.map_mgr = map_mgr
        cls.grid = grid
        start = tuple(start_pos)
        goal = tuple(end_pos)

        came_from = cls.search(start, goal)

        path = cls.reconstruct_path(came_from, start, goal)

        return path

    @classmethod
    def search(cls, start, goal):
        """..."""
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        came_from[start] = None

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in cls.neighbors(current, goal):
                if next not in came_from:
                    priority = cls.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current
        return came_from


class AStarSearch(PathFinders):
    """..."""

    @classmethod
    def new_search(cls, map_mgr, grid, start_pos, end_pos):
        """..."""
        cls.map_mgr = map_mgr
        cls.grid = grid
        start = tuple(start_pos)
        goal = tuple(end_pos)

        came_from, cost_so_far = cls.search(start, goal)
        try:
            path = cls.reconstruct_path(came_from, start, goal)
        except KeyError:
            raise KeyError
        return path

    @classmethod
    def cost(cls, node):
        """..."""
        return 1

    @classmethod
    def search(cls, start, goal):
        """..."""
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            for next in cls.neighbors(current, goal=goal):
                new_cost = cost_so_far[current] + cls.cost(next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + cls.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

            if current == goal:
                break

        return came_from, cost_so_far


if __name__ == '__main__':
    GreedySearch.test()
