class Position:
    # pygame.Rect

    def __init__(self, pos):
        self.x, self.y = pos

    @property
    def pos(self):
        return (self.x, self.y)

    def __mod__(self, n):
        try:
            return Position((self.x % n[0], self.y % n[1]))
        except TypeError:
            return Position((self.x % n, self.y % n))

    def __truediv__(self, n):
        try:
            return Position((self.x / n[0], self.y / n[1]))
        except TypeError:
            return Position((self.x / n, self.y / n))

    def __mul__(self, n):
        try:
            return Position((self.x * n[0], self.y * n[1]))
        except TypeError:
            return Position((self.x * n, self.y * n))

    def __floordiv__(self, n):
        try:
            return Position((self.x // n[0], self.y // n[1]))
        except TypeError:
            return Position((self.x // n, self.y // n))

    def __add__(self, n):
        try:
            return Position((self.x + n[0], self.y + n[1]))
        except TypeError:
            return Position((self.x + n, self.y + n))
    """
    def __add__(self, n):
        try:
            return Position((self.x + n[0], self.y + n[1]))
        except TypeError:
            try:
                return Position((self.x + n, self.y + n))
            except TypeError:
                if n is None:
                    return self.pos
    """

    def __sub__(self, n):
        try:
            return Position((self.x - n[0], self.y - n[1]))
        except TypeError:
            return Position((self.x - n, self.y - n))

    def __eq__(self, n):
        try:
            return (self.x, self.y) == n
        except TypeError:
            return self.x == n.x and self.y == n.y

    def __iter__(self):
        return iter((self.x, self.y))

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return "Position(x:{x}, y:{y})".format(x=self.x, y=self.y)

    def __str__(self):
        return "Position(x:{x}, y:{y})".format(x=self.x, y=self.y)

    def __getitem__(self, key):
        return self.pos[key]


if __name__ == '__main__':
    pos = Position((2, 4))
    print(pos == (2, 4))
    print(pos == Position((2, 4)))
    d = {}
    d[pos] = 1
    print(pos + (1, -1))
    print(
        Position((2, 4)) != Position((2, 5)),
        Position((2, 4)) == Position((2, 5)))
    print(tuple(pos))
    path = [(2, 4), (1, 3)]
    print(pos in path)

    print(pos % 3)
    print(pos + 2)
    print(pos * 2)

    assert(Position((1, 1)) == (1, 1))
    assert((1, 1) == Position((1, 1)))

    assert(Position((1, 1)) + (1, 1) == (2, 2))
    assert(Position((1, 1)) + (1, 1) == Position((2, 2)))

    # order matters...
    # -> can only concatenate tuple (not "Position") to tuple
    # assert((1, 1) + Position((1, 1)) == (2, 2))

    assert(Position((3, 2)) - (1, 1) == (2, 1))
    assert(Position((3, 2)) - (1, 1) == Position((2, 1)))

    print(pos + None)
