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


class AStarSearch:
    @classmethod
    def new_search(cls, map_mgr, grid, start_pos, end_pos):
        cls.map_mgr = map_mgr
        cls.grid = grid
        start = tuple(start_pos)
        goal = tuple(end_pos)

        came_from, cost_so_far = cls.search(start, goal)
        path = cls.reconstruct_path(came_from, start, goal)
        return path

    @staticmethod
    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    @classmethod
    def cost(cls, node):
        return 1

    @classmethod
    def search(cls, start, goal):
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

    @staticmethod
    def reconstruct_path(came_from, start, goal):
        current = goal
        reconstruct_path = [current]
        while current != start:
            current = came_from[current]
            reconstruct_path.append(current)
        reconstruct_path.reverse()
        return reconstruct_path

    @classmethod
    def neighbors(cls, node, goal):
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        result = []
        for dir in dirs:
            neighbor = (node[0] + dir[0], node[1] + dir[1])
            if cls.map_mgr.valid_tile(neighbor) or neighbor == goal:
                result.append(neighbor)
        return result
