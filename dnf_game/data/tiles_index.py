"""..."""

from dnf_game.data.constants import TILE_W

_INDEX = {
    "floor": {"start": (0, 16), "var": 16, "pos": 16},
    "hall": {"start": (0, 16), "var": 16, "pos": 16},
    "wall": {"start": (0, 32), "var": 8, "pos": 16},

    "stair_down": {"start": (0, 40), "var": 2, "pos": 1},
    "ui_window": {"start": (0, 42), "var": 3, "pos": 3},

    "bmp_font": {"start": (0, 0), "var": 16, "pos": 16}
}


class TileIndexEntry(object):
    """..."""

    def __init__(self, start, var, pos):
        """..."""
        self.start = start
        self.var = var
        self.pos = pos

    def __repr__(self):
        """..."""
        return self.__str__()

    def __str__(self):
        """..."""
        return "%s(start=%s, var=%s, pos=%s)" % (
            self.__class__.__name__, self.start, self.var, self.pos)


class TilesetIndex(object):
    """..."""

    index = {name: TileIndexEntry(**data) for name, data in _INDEX.items()}

    @staticmethod
    def get_data(name):
        """..."""
        return TilesetIndex.index[name]

    @staticmethod
    def get_var(tile):
        entry = TilesetIndex.get_data(tile.name)
        return entry.var

    @staticmethod
    def get_tile_rect(*, tile=None, pos=None, var=None, _id=None):
        """..."""
        try:
            data = TilesetIndex.get_data(tile)
        except KeyError:
            data = TilesetIndex.get_data("bmp_font")
            tile = None

        if tile is None and _id is None:
            raise ValueError("Either 'tile' or '_id' must be provided.")
        elif tile is None and _id is not None:
            try:
                _id = int(_id)
            except TypeError:
                _id = ord(_id)

            x = (_id % data.pos) * TILE_W
            y = (_id // data.pos) * TILE_W
        else:
            x = (pos + data.start[0]) * TILE_W
            y = (var + data.start[1]) * TILE_W

        return (x, y, TILE_W, TILE_W)
