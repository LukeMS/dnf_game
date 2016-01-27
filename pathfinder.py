import heapq


class PriorityQueue:

    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class PathFinders:

    @staticmethod
    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def reconstruct_path(came_from, start, goal):
        current = goal
        reconstruct_path = [current]
        while current != start:
            current = came_from[current]
            reconstruct_path.append(current)
        reconstruct_path.reverse()
        return reconstruct_path

    def neighbors(self, node, goal, diagonals, check_obj, max_distance):
        lst = []
        x0, y0 = node
        if diagonals:
            _n_pos = []
            for x1 in [-1, 0, 1]:
                for y1 in [-1, 0, 1]:
                    if x1 and y1:
                        _n_pos.append((x0 + x1, y0 + y1))
        else:
            _n_pos = [
                (x0 - 1, y0),  # left
                (x0, y0 - 1),  # top
                (x0, y0 + 1),  # bottom
                (x0 + 1, y0),  # right
            ]
        """
        for x1 in [-1, 0, 1]:
            for y1 in [-1, 0, 1]:
                print(chr(self.map_mgr.grid[x0 + x1, y0 + y1].id),
                    sep="", end="")
            print()
        """
        print("node, goal, _n_pos:", node, goal, _n_pos)
        print("diagonals, check_obj, max_distance",
              diagonals, check_obj, max_distance)

        for n in _n_pos:
            if n == goal:
                lst.append(n)
            elif self.map_mgr.valid_tile(
                n, goal=goal,
                check_obj=check_obj, max_distance=max_distance
            ):
                lst.append(n)

        print("list:", lst)
        return lst


class AStarSearch(PathFinders):

    def __init__(self, map_mgr, grid):
        self.map_mgr = map_mgr
        self.grid = grid

    def new_search(self, start_pos, end_pos,
                   diagonals, check_obj, max_distance):
        start = tuple(start_pos)
        goal = tuple(end_pos)
        # self.cost = cost_func or self._cost
        self.diagonals = diagonals

        came_from, cost_so_far = self.search(
            start, goal,
            diagonals=diagonals, check_obj=check_obj,
            max_distance=max_distance)
        try:
            path = self.reconstruct_path(came_from, start, goal)
        except KeyError:
            raise KeyError
        return path

    def cost(self, node, current):
        cost = 1

        if node[0] < current[0]:
            cost -= .1
        elif node[0] > current[0]:
            cost += .1

        if node[1] < current[1]:
            cost -= .1
        elif node[1] > current[1]:
            cost += .1

        return cost

    def search(self, start, goal, diagonals, check_obj, max_distance):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            neighbors = self.neighbors(
                current, goal=goal, diagonals=diagonals, check_obj=check_obj,
                max_distance=max_distance)
            print("neighbors:", neighbors)
            for next in neighbors:
                new_cost = cost_so_far[current] + self.cost(next, current)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

            if current == goal:
                break

        return came_from, cost_so_far
