"""..."""


class TileFx:
    """Keeps combinations of coordinates, color and duration of tile effects.

    When updated, every list will be checked, and its member's duration
    decreased by one (removing it if < 1).
    When used to check if it contains a coordinate, returns the color of
    the first effect found for that coordinate; if nothing is found, returns
    None.
    When adding a new effect it is stored after the last added effect of same
    duration (if it exists, if not, it goes to the last position).
    """

    def __init__(self, scene):
        """..."""
        self._scene = scene

    def data(self):
        """..."""
        return self._scene.levels[self._scene.current_level]['tile_fx']

    def add(self, coord, color, duration):
        """Used to store an effect on the container.

        coord: a list of tuple coordinates (x, y)
        color: a tuple of three values (r, g, b)
        duration: an integer, how many turns the effect should last.
        """
        data = self.data()

        index = len(data)
        for i, fx in enumerate(data):
            if fx['duration'] > index:
                index = i
                break

        data.insert(
            index,
            {
                "coord": coord,
                "color": color,
                "duration": duration})

    def update(self):
        """Reduce the duration of the members duration by one.

        Remove it if the duration is less then one.
        """
        data = self.data()

        for i in range(len(data) - 1, -1, -1):
            fx = data[i]
            if fx['duration'] < 1:
                data.pop(i)
            else:
                fx['duration'] -= 1

    def get(self, coord, throwback=None):
        """Return the color of the effect for a given coordinate.

        It returns None as default if the coordinate doesn't have an effect
        stored.
        If you want it to return something else (overriding the default value),
        pass it as throwback.
        """
        data = self.data()

        pos = x, y = coord
        # print(pos)
        for fx in data:
            if pos in fx['coord']:
                return fx['color']
        return throwback


if __name__ == '_data__':
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

    for i in range(40):
        print("(0, 2): {}, (1, 3):{}, (3, 0): {}".format(
            tile_fx.get((0, 2)),
            tile_fx.get((1, 3)),
            tile_fx.get((3, 0))
        ))
        tile_fx.update()
