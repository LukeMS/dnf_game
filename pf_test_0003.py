import os
import random
import heapq

clear = lambda: os.system('cls' if (os.name == 'nt') else 'clear')


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class Graph:

    grid = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1,
            0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1,
            0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1,
            0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1,
            1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1,
            1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1,
            0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1,
            0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1,
            0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1,
            1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0,
            0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
            0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0,
            0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1,
            1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1,
            1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1,
            1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1,
            0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1,
            0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1,
            1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1,
            1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1,
            0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
            0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1,
            0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    chars = {0: ' ', 1: "#", 2: "@", 3: ".", 4: "~", 5: "!"}
    walkable = [0, 2, 3, 4, 5]
    weights = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1}

    def __init__(self):
        while True:
            start = (
                random.randint(0, len(self.grid[0]) - 1),
                random.randint(0, len(self.grid) - 1))
            if self.valid_node(start):
                self.set_cell_at(start, value=2)
                break
        while True:
            goal = (
                random.randint(0, len(self.grid[0]) - 1),
                random.randint(0, len(self.grid) - 1))
            if self.valid_node(goal):
                self.set_cell_at(goal, value=5)
                break
        self.draw()
        came_from, cost_so_far = self.a_star_search(start, goal)
        path = self.reconstruct_path(came_from, start, goal)
        for node in reversed(path):
            if node not in (start, goal):
                self.set_cell_at(node, 4)
            self.draw()

    def valid_node(self, node):
        return (
            0 <= node[0] < len(self.grid[0]) and
            0 <= node[1] < len(self.grid) and
            self.get_cell_at(node) in self.walkable
        )

    def get_cell_at(self, pos):
        return self.grid[pos[1]][pos[0]]

    def set_cell_at(self, pos, value):
        self.grid[pos[1]][pos[0]] = value

    @staticmethod
    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def cost(self, node):
        return self.weights[self.get_cell_at(node)]

    def a_star_search(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            self.draw()
            current = frontier.get()

            if current == goal:
                break

            for next in self.neighbors(current):
                new_cost = cost_so_far[current] + self.cost(next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    if next != goal:
                        self.set_cell_at(next, 3)
                    came_from[next] = current

        return came_from, cost_so_far

    @staticmethod
    def reconstruct_path(came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def neighbors(self, node):
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        result = []
        for dir in dirs:
            neighbor = (node[0] + dir[0], node[1] + dir[1])
            if self.valid_node(neighbor):
                result.append(neighbor)
        return result

    def _compute_f_cost(self, node, goal):
        return node.g_cost + self._cost_to_goal(node, goal)

    def _cost_to_goal(self, node, goal):
        return self.manhattan(node.coord, goal)

    def draw(self):
        clear()
        for row in self.grid:
            for col in row:
                print(self.chars[col], sep="", end="")
            print()

graph = Graph()
