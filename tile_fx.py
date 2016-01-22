import fov
from constants import MAP_COLS, MAP_ROWS


class AreaFx:
    def get_area(self, grid, pos, radius):
        self.grid = grid

        x, y = pos

        self.area = []

        fov.fieldOfView(
            x, y, MAP_COLS, MAP_ROWS,
            radius, self.func_visit, self.func_blocked
        )

        return self.area

    def func_visit(self, x, y):
        self.area.append((x, y))

    def func_blocked(self, x, y):
        return self.grid[x, y].block_mov


class TileFx:
    """Contains combinations of coordinates, color and duration of tile
    effects. When updated, every list will be checked, its duration decreased
    by one (removing entries with duration 0).
    When used to check if contains a coordinate, returns the color of the first
    effect found for that coordinate; if nothing is found, returns None.
    """
    _main = []

    def add(self, coord, color, duration):
        index = len(self._main)
        for i, fx in enumerate(self._main):
            if fx['duration'] > index:
                index = i
                break

        self._main.insert(
            index,
            {
                "coord": coord,
                "color": color,
                "duration": duration})

    def update(self):
        for i in range(len(self._main) - 1, -1, -1):
            fx = self._main[i]
            if fx['duration'] < 1:
                self._main.pop(i)
            else:
                fx['duration'] -= 1

    def get(self, coord, throwback=None):
        pos = x, y = coord
        # print(pos)
        for fx in self._main:
            if pos in fx['coord']:
                return fx['color']
        return throwback


if __name__ == '__main__':
    tile_fx = TileFx()

    tile_fx.add(
        [(0, 2), (1, 4)],
        'red', 1)

    tile_fx.add(
        [(1, 3), (2, 5)],
        'blue', 2)

    tile_fx.add(
        [(0, 2), (3, 0)],
        'yellow', 3)

    for i in range(4):
        print("(0, 2): {}, (1, 3):{}, (3, 0): {}".format(
            tile_fx.get((0, 2)),
            tile_fx.get((1, 3)),
            tile_fx.get((3, 0))
        ))
        tile_fx.update()
