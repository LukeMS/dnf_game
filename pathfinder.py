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

    def valid_tile(self, pos):
        if not (
            pos is not None and
            0 <= pos[0] < self.width
            and 0 <= pos[1] < self.height
        ):
            return False
        return True

    def neighbors(self, node, goal=None, diagonals=True,
                  check_obj=True, max_distance=None):
        lst = []
        x0, y0 = node
        if self.diagonals or diagonals:
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
        # print(node, goal, _n_pos)

        for n in _n_pos:
                # try:
                valid = (self.map_mgr.valid_tile(n, goal,
                         check_obj=False, max_distance=None) or n == goal)
                """
                except:
                    print('map_mgr failed')
                    valid = self.valid_tile or n == goal
                """
                if valid:
                    lst.append(n)
        # print("\n", lst)
        return lst


class AStarSearch(PathFinders):

    def __init__(self, map_mgr, grid):
        self.map_mgr = map_mgr

    def new_search(self, start_pos, end_pos, diagonals=True,
                   check_obj=True, max_distance=10):
        start = tuple(start_pos)
        goal = tuple(end_pos)
        # self.cost = cost_func or self._cost
        self.diagonals = diagonals

        came_from, cost_so_far = self.search(start, goal)
        try:
            path = self.reconstruct_path(came_from, start, goal)
        except KeyError:
            raise KeyError
        return path

    def cost(self, node):
        return 1

    def search(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            for next in self.neighbors(current, goal=goal,
                                       diagonals=self.diagonals):
                new_cost = cost_so_far[current] + self.cost(next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

            if current == goal:
                break

        return came_from, cost_so_far
