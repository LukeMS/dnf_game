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

    @property
    def data(self):
        """..."""
        return self._scene.current_level.tile_fx

    def add(self, *, coord, color, duration):
        """Used to store an effect on the container.

        coord: a list of tuple coordinates (x, y)
        color: a tuple of three values (r, g, b)
        duration: an integer, how many turns the effect should last.
        """
        data = self.data

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
        data = self.data

        for i in range(len(data) - 1, -1, -1):
            fx = data[i]
            duration = fx['duration']
            if not duration:
                data.pop(i)
            else:
                if duration > 0:
                    fx['duration'] -= 1

    def get(self, coord, default=None):
        """Return the color of the effect for a given coordinate.

        If the coordinate doesn't have an effect stored, a specified
        default value (or None) is returned.
        """
        data = self.data

        pos = x, y = coord
        # print(pos)
        for fx in data:
            if pos in fx['coord']:
                return fx['color']
        return default

    def __str__(self):
        return "\n".join(
            ", ".join("{}:({})".format(k, v) for k, v in list(turn.items()))
            for turn in self.data
        )


if __name__ == '__main__':

    class CurrentLevel:
        """..."""

        def __init__(self):
            """..."""
            self.tile_fx = []

    class DummyScene:
        """..."""

        def __init__(self):
            """..."""
            self.current_level = CurrentLevel()
            self.tile_fx = TileFx(scene=self)

    scene = DummyScene()
    tile_fx = scene.tile_fx

    tile_fx.add(coord=[(0, 2), (1, 4)], color='red', duration=1)
    tile_fx.add(coord=[(1, 3), (2, 5)], color='blue', duration=2)
    tile_fx.add(coord=[(0, 2), (3, 0)], color='yellow', duration=3)
    tile_fx.add(coord=[(0, 2), (3, 0)], color='green', duration=-1)

    for t in range(1, 5 + 1):
        print("Turn:", t)
        print(tile_fx, "\n")
        tile_fx.update()
