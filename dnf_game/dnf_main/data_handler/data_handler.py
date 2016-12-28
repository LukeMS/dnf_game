"""Helper functions to open and handle bz2 compressed json file's content."""

import os

from dnf_game.util.ext.namedtuple_with_abc import namedtuple
from dnf_game.data.constants import TILE_W
from dnf_game.data import specific_armors, specific_weapons, tiles_index
from dnf_game.data.colors import COLORS
from dnf_game.util import packer, dnf_path, SingletonMeta
from dnf_game.util.ext.namedtuple_with_abc import ntuple_from_dict


PATH = dnf_path()

NAMES_PATH = os.path.join(PATH, 'data', 'names.bzp')
STD_ARMORS_PATH = os.path.join(PATH, 'data', 'armors.bzp')
STD_WEAPONS_PATH = os.path.join(PATH, 'data', 'weapons.bzp')
TILESET_MAP = os.path.join(PATH, "resources", "tilesets",
                           "packed_tileset_32_map.txt")


# ########################
# names
def get_names():
    """Return all names.

    Utility function to access data names through the singleton.
    """
    return DataHandler().names


# ########################
# colors
def get_colors():
    """Return all colors.

    Utility function to access data names through the singleton.
    """
    return DataHandler().colors


def get_color(color):
    """Return a specific color.

    Utility function to access data names through the singleton.
    """
    return getattr(get_colors(), color)


# ########################
# tileset
def get_tile_data(tile):
    """Return the tileset data for a specific entry.

    Utility function to access data names through the singleton.
    """
    return DataHandler().get_tile_data(tile)


def get_tile_var(tile):
    """Return the tile variaton from the tileset index.

    Utility function to access data names through the singleton.
    """
    return DataHandler().get_tile_var(tile)


def get_tile_rect(*, tile=None, pos=None, var=None, _id=None):
    """Return the tile rect from the tileset index.

    If the named tile is not found the default bitmap font tileset is used
    instead and a matching character for the tile id is returned.
    """
    return DataHandler().get_tile_rect(
        tile=tile, pos=pos, var=var, _id=_id)


# ########################
# armors
def get_all_armor_names():
    """Return all armor names.

    Utility function to access data names through the singleton.
    """
    return DataHandler().armor_names


def get_all_armors():
    """Return all armors.

    Utility function to access data names through the singleton.
    """
    return DataHandler().armors


def get_armor(item):
    """Return the armor requested.

    Utility function to access data names through the singleton.
    """
    return DataHandler().get_armor(item)


# ########################
# weapons
def get_all_weapon_names():
    """Return all weapon names.

    Utility function to access data names through the singleton.
    """
    return DataHandler().weapon_names


def get_all_weapons():
    """Return all weapons.

    Utility function to access data names through the singleton.
    """
    return DataHandler().weapons


def get_weapon(item):
    """Return the weapon requested.

    Utility function to access data names through the singleton.
    """
    return DataHandler().get_weapon(item)


# ########################
# The DataHandler itself
class DataHandler(metaclass=SingletonMeta):
    """A singleton DataHandler that caches the data required.

    Its purpose is to avoid redundant calls to disk.
    """

    # ########################
    # names
    @property
    def names(self):
        """Return all names."""
        if getattr(self, "_names", None) is None:
            print("%s: caching names" % self.__class__.__name__)
            self._names = packer.unpack_json(NAMES_PATH)
        return self._names

    # ########################
    # colors
    @property
    def colors(self):
        """Return all colors."""
        if getattr(self, "_colors", None) is None:
            print("%s: caching colors" % self.__class__.__name__)
            self._colors = ntuple_from_dict(COLORS)
        return self._colors

    # ########################
    # tileset
    @property
    def tileset_index(self):
        """Return data from the whoel tileset."""
        if getattr(self, "_tileset_index", None) is None:
            print("%s: loading tileset data" % self.__class__.__name__)
            self.create_tileset_index()
        return self._tileset_index

    def create_tileset_entry(self, l):
        """..."""
        name, data = l.split(" = ")
        alias = tiles_index.NAMES[name]
        pixel_data = data.split()
        x, y, w, h = (int(i) // TILE_W for i in pixel_data)
        return ((alias, TilesetEntry(name=alias, x=x, y=y, w=w, h=h)),)

    def parse_tileset_map(self):
        """..."""
        with open(TILESET_MAP) as f:
            l = f.read().splitlines()
        return l

    def create_tileset_index(self):
        """..."""
        lst = self.parse_tileset_map()
        create_tileset_entry = self.create_tileset_entry
        self._tileset_index = {
            k: v
            for line in lst
            for k, v in create_tileset_entry(line)
        }

    def get_tile_data(self, tile):
        """Return the tileset data for a specific entry."""
        return self.tileset_index[tile]

    def get_tile_var(self, tile):
        """Return the tile variaton from the tileset index."""
        data = self.get_tile_data(tile)
        return data.var

    def get_tile_rect(self, *, tile=None, pos=None, var=None, _id=None):
        """Return the tile rect from the tileset index.

        If the named tile is not found the default bitmap font tileset is used
        instead and a matching character for the tile id is returned.
        """
        try:
            data = get_tile_data(tile)
        except KeyError:
            print("no tileset data")
            data = get_tile_data("bmp_font")
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
            x = (pos + data.x) * TILE_W
            y = (var + data.y) * TILE_W

        return (x, y, TILE_W, TILE_W)

    # ########################
    # armors
    @property
    def armors(self):
        """Return all armors."""
        if getattr(self, "_armors", None) is None:
            print("%s: caching armors" % self.__class__.__name__)
            std = packer.unpack_json(STD_ARMORS_PATH)
            spec = specific_armors.SPECIFIC
            self._armors = {**spec, **std}
        return self._armors

    @property
    def armor_names(self):
        """Return all armor names."""
        return self.armors.keys()

    def get_armor(self, item):
        """Return the armor requested."""
        return self.armors.__getitem__(item)

    # ########################
    # weapons
    @property
    def weapons(self):
        """Return all weapons."""
        if getattr(self, "_weapons", None) is None:
            print("%s: caching weapons" % self.__class__.__name__)
            std = packer.unpack_json(STD_WEAPONS_PATH)
            spec = specific_weapons.SPECIFIC
            self._weapons = {**spec, **std}
        return self._weapons

    @property
    def weapon_names(self):
        """Return all weapon names."""
        return self.weapons.keys()

    def get_weapon(self, item):
        """Return the weapon requested."""
        return self.weapons.__getitem__(item)

    def __getstate__(self):
        """Prevent pickling by returning None."""
        return None


class TilesetEntry(namedtuple.abc):
    """Utility class to store and read tileset entry data."""

    _fields = "name x y w h"

    def __repr__(self):
        """..."""
        return ('{0.__class__.__name__}'
                '(name={0.name},'
                ' x={0.x},'
                ' y={0.y},'
                ' pos={0.pos},'
                ' var={0.var})'.format(self))

    @property
    def width(self):
        """Width of the tileset area, in columns."""
        return self.w

    @property
    def pos(self):
        """Number of different positions the tile has.

        Same as width in columns of the area.
        """
        return self.w

    @property
    def height(self):
        """Height of the tileset area, in rows."""
        return self.h

    @property
    def var(self):
        """Number of variations the tile has.

        Same as height in rows of the area.
        """
        return self.h

if __name__ == '__main__':
    """
    a = DataHandler()
    a.weapons
    a.colors
    b = DataHandler()
    b.weapons
    c = b.colors
    print(c.black)
    print(get_colors().black)
    print(get_color("black"))
    """
    a = DataHandler()
    for i in range(1000):
        try:
            data = get_tile_data("floor")
        except KeyError as e:
            from dnf_game.util import describe_error
            describe_error(e, "index %d" % i, DataHandler().tileset_index)
            raise
