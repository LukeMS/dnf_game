from priorityqueueset import PriorityQueueSet
import time


def moveCost(pos1, pos2):
    if not pos1.x == pos2.x:
        if not pos1.y == pos2.y:
            return 12
        return 9
    return 8


def manhattan(pos1, pos2):
    minX = min(pos1.x, pos2.x)
    maxX = max(pos1.x, pos2.x)
    minY = min(pos1.y, pos2.y)
    maxY = max(pos1.y, pos2.y)

    xLen = maxX - minX
    yLen = maxY - minY

    return (xLen + yLen) * 10


class findPath(object):

    def __init__(self, map, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos
        self.map = map

        def getNeighbors(pos):
            l = list()
            for n in pos.neighbors():
                if not (n.x >= self.map.width or n.y >= self.map.height):
                    if not self.map.getCellAtPos(n).blockedByTerrain \
                            or n == endPos:
                        l.append(n)
            return l

        PF = PathFinder(getNeighbors, moveCost, manhattan)
        iterable = PF.compute_path(startPos, endPos)
        self.iter = iterable


class PathFinder(object):
    """
        "The code is in the public domain - do whatever you wish with it."
            --http://eli.thegreenplace.net/2009/01/09/writing-a-game-in-python-with-pygame-part-iii/

        Computes a path in a graph using the A* algorithm.

        Initialize the object and then repeatedly compute_path to
        get the path between a start point and an end point.

        The points on a graph are required to be hashable and
        comparable with __eq__. Other than that, they may be
        represented as you wish, as long as the functions
        supplied to the constructor know how to handle them.
    """

    def __init__(self, successors, move_cost, heuristic_to_goal):
        """ Create a new PathFinder. Provided with several
            functions that represent your graph and the costs of
            moving through it.

            successors:
                A function that receives a point as a single
                argument and returns a list of "successor" points,
                the points on the graph that can be reached from
                the given point.

            move_cost:
                A function that receives two points as arguments
                and returns the numeric cost of moving from the
                first to the second.

            heuristic_to_goal:
                A function that receives a point and a goal point,
                and returns the numeric heuristic estimation of
                the cost of reaching the goal from the point.
        """
        self.t1 = time.clock()

        self.successors = successors
        self.move_cost = move_cost
        self.heuristic_to_goal = heuristic_to_goal

    def compute_path(self, start, goal):
        """ Compute the path between the 'start' point and the
            'goal' point.

            The path is returned as an iterator to the points,
            including the start and goal points themselves.

            If no path was found, an empty list is returned.
        """
        #
        # Implementation of the A* algorithm.
        #
        closed_set = {}

        start_node = self._Node(start)
        start_node.g_cost = 0
        start_node.f_cost = self._compute_f_cost(start_node, goal)

        open_set = PriorityQueueSet()
        open_set.add(start_node)

        while len(open_set) > 0:
            # Remove and get the node with the lowest f_score from
            # the open set
            #

            if len(open_set) > 100:
                t2 = time.clock()
                timeWasted = t2 - self.t1
                raise ValueError('path too long, wasted %f sec' % timeWasted)

            curr_node = open_set.pop_smallest()

            if curr_node.coord == goal:
                return self._reconstruct_path(curr_node)

            closed_set[curr_node] = curr_node

            for succ_coord in self.successors(curr_node.coord):
                succ_node = self._Node(succ_coord)
                succ_node.g_cost = self._compute_g_cost(curr_node, succ_node)
                succ_node.f_cost = self._compute_f_cost(succ_node, goal)

                if succ_node in closed_set:
                    continue

                if open_set.add(succ_node):
                    succ_node.pred = curr_node

        return []

    ########################## PRIVATE ##########################

    def _compute_g_cost(self, from_node, to_node):
        return (from_node.g_cost +
                self.move_cost(from_node.coord, to_node.coord))

    def _compute_f_cost(self, node, goal):
        return node.g_cost + self._cost_to_goal(node, goal)

    def _cost_to_goal(self, node, goal):
        return self.heuristic_to_goal(node.coord, goal)

    def _reconstruct_path(self, node):
        """ Reconstructs the path to the node from the start node
            (for which .pred is None)
        """
        pth = [node.coord]
        n = node
        while n.pred:
            n = n.pred
            pth.append(n.coord)

        return reversed(pth)

    class _Node(object):
        """ Used to represent a node on the searched graph during
            the A* search.

            Each Node has its coordinate (the point it represents),
            a g_cost (the cumulative cost of reaching the point
            from the start point), a f_cost (the estimated cost
            from the start to the goal through this point) and
            a predecessor Node (for path construction).

            The Node is meant to be used inside PriorityQueueSet,
            so it implements equality and hashinig (based on the
            coordinate, which is assumed to be unique) and
            comparison (based on f_cost) for sorting by cost.
        """

        def __init__(self, coord, g_cost=None, f_cost=None, pred=None):
            self.coord = coord
            self.g_cost = g_cost
            self.f_cost = f_cost
            self.pred = pred

        def __eq__(self, other):
            return self.coord == other.coord

        def __cmp__(self, other):
            return cmp(self.f_cost, other.f_cost)

        def __hash__(self):
            return hash(self.coord)

        def __str__(self):
            return 'N(%s) -> g: %s, f: %s' % (self.coord,
                                              self.g_cost,
                                              self.f_cost)

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
    """ WARNING:

    This code picks two arbitrary points on the map, which
    in many cases are very far apart in terms of a path.
    If this runs for > 10 seconds or so you should ctrl+c and try again
    """

    import sys
    from ascii_map import Map
    from constants import *
    from position import Position
    import random
    from random import randint

    START_TYPE = 9999
    END_TYPE = 99999
    PATH_TYPE = 999999

    random.seed()

    w, h = (60, 79)
    map = Map(width=w, height=h)

    for i in range(len(map.map)):
        for v in range(len(map.map[i])):
            if map.map[i][v].type == DUNGEON_DOOR:
                map.map[i][v].blockedByTerrain = False

    started, finished = None, None
    startPos, endPos = None, None

    while 1:
        pos = Position(randint(0, w - 1), randint(0, h - 1))
        if started is None:
            if map.getCellAtPos(pos).type == DUNGEON_FLOOR:
                startPos = pos
                started = 1
        elif finished is None:
            if map.getCellAtPos(pos).type == DUNGEON_FLOOR:
                xDiff = max(startPos.x, pos.x) - min(startPos.x, pos.x)
                yDiff = max(startPos.y, pos.y) - min(startPos.y, pos.y)
                if xDiff + yDiff < 20:
                    endPos = pos
                    finished = 1

        else:
            break

    path = findPath(map, startPos, endPos)
    for pos in path.iter:
        map.getCellAtPos(pos).type = PATH_TYPE

    map.getCellAtPos(startPos).type = START_TYPE
    map.getCellAtPos(endPos).type = END_TYPE

    for x in range(len(map.map)):
        for y in range(len(map.map[x])):
            if map.map[x][y].type == DUNGEON_WALL:
                sys.stdout.write('#')
            elif map.map[x][y].type == DUNGEON_FLOOR:
                sys.stdout.write(' ')
            elif map.map[x][y].type == DUNGEON_DOOR:
                sys.stdout.write('D')
            elif map.map[x][y].type == START_TYPE:
                sys.stdout.write('S')
            elif map.map[x][y].type == END_TYPE:
                sys.stdout.write('F')
            elif map.map[x][y].type == PATH_TYPE:
                sys.stdout.write('~')
        print('\n', end=' ')
