#import pygame


class Position:
    # pygame.Rect

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __truediv__(self, n):
        if isinstance(n, tuple):
            return Position(self.x / n[0], self.y / n[1])
        elif isinstance(n, (int, float)):
            return Position(self.x / n, self.y / n)

    def __floordiv__(self, n):
        if isinstance(n, tuple):
            return Position(int(self.x // n[0]), int(self.y // n[1]))
        elif isinstance(n, (int, float)):
            return Position(int(self.x // n), int(self.y // n))

    def __add__(self, n):
        if isinstance(n, tuple):
            return Position(int(self.x + n[0]), int(self.y + n[1]))
        elif isinstance(n, (int, float)):
            return Position(int(self.x + n), int(self.y + n))

    def __eq__(self, n):
        if isinstance(n, tuple):
            return (self.x, self.y) == n
        elif isinstance(n, Position):
            return self.x == n.x and self.y == n.y

    def __iter__(self):
        for coord in [self.x, self.y]:
            yield coord

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return "Position{}".format((self.x, self.y))

    def __str__(self):
        return "x, y: ({}, {})".format(self.x, self.y)

    def _neighbors(self):
        lst = []
        changes_dict = dict()
        changes_lst = [-1, 0, 1]
        for i in changes_lst:
            changes_dict[i] = changes_lst

        for x in changes_dict:
            for y in changes_dict[x]:
                if x == 0 and y == 0:
                    continue
                lst.append(Position(self.x + x, self.y + y))
        return lst


if __name__ == '__main__':
    pos = Position(2, 4)
    print(pos == (2, 4))
    #print(pos == Position(2, 4))
    #d = {}
    #d[pos] = 1
    #print(pos + (1, -1))
    print(Position(2, 4) == Position(2, 5))
