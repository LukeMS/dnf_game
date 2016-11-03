"""..."""

import sys
import os

import pygame
import weakref

from constants import TILESET, TILE_W, TILE_H

BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "resources")


class Resources(object):
    """..."""

    _names = {}

    def __new__(cls, **kwargs):
        """Prevent creation of more then one instance."""
        if not hasattr(cls, '_instance'):
            print("Starting", cls.__name__)
            cls._instance = super().__new__(cls)
        else:
            e = NotImplementedError(
                "Use {} ".format(cls.__name__) +
                "as singleton class intead of creating new instances.")
            raise e
        return cls._instance

    @classmethod
    def __init__(cls, loader, path, types, weak_ref=True):
        """..."""
        cls._names = cls._index(path, types)
        if weak_ref:
            cls.cache = weakref.WeakValueDictionary()
        else:
            cls.cache = {}
        cls.loader = loader

    @classmethod
    def __getattr__(cls, name):
        """..."""
        try:
            obj = cls.cache[name]
        except KeyError:
            obj = cls.loader(cls._names[name])
            cls.cache[name] = obj
        return obj

    @classmethod
    def get(cls, name):
        """..."""
        return cls.__getattr__(name)

    @classmethod
    def _index(cls, path, types):
        """..."""
        _names = {}
        if sys.version_info >= (3, 5):
            # Python version >=3.5 supports glob
            import glob
            for obj_type in types:
                for filename in glob.iglob(
                    (path + '/**/' + obj_type), recursive=True
                ):
                    f_base = os.path.basename(filename)
                    _names.update({f_base: filename})
        else:
            # Python version <=3.4
            import fnmatch

            for root, dirnames, filenames in os.walk(path):
                for obj_type in types:
                    for f_base in fnmatch.filter(filenames, obj_type):
                        filename = os.path.join(root, f_base)
                        _names.update({f_base: filename})
        return _names

    def __getstate__(self):
        """..."""
        return None


class ImageBase(Resources):
    """..."""

    @classmethod
    def __getattr__(cls, name):
        """..."""
        try:
            img = cls.cache[name]
        except KeyError:
            # print(name, name in cls._names)
            img = cls.loader(cls._names[name]).convert_alpha()
            cls.cache[name] = img
        return img


class Images(ImageBase):
    """..."""

    @classmethod
    def __init__(cls, path=BASE_PATH, types=None):
        """..."""
        types = types if types else ['*.jpg', '*.png', '*.bmp']
        super().__init__(
            loader=pygame.image.load,
            path=path,
            types=types)


class Tilesets(ImageBase):
    """..."""

    _tilesets = {}

    @classmethod
    def __init__(cls, path=os.path.join(BASE_PATH, "tilesets"), types=None):
        """..."""
        types = types if types else ['*.jpg', '*.png', '*.bmp']
        cls.loader = pygame.image.load
        cls._names = cls._index(path=path, types=types)

        cls.cache = {}

        tiles = {}
        for k in cls._names.keys():
            if k.startswith('_tile'):
                k_fields = k.split('$')

                id = int(k_fields[0].replace('_tile', ''))
                size = int(k_fields[2].replace('px', ''))
                theme = k_fields[1]
                var = int(k_fields[3].replace('v', ''))

                tiles.setdefault(id, {})
                tiles[id][size, theme] = {
                    'var': var,
                    'img': cls.get(k)
                }
        cls.tiles = tiles

        _tileset = cls.get_set()
        cls.tileset_width, cls.tileset_height = _tileset.get_size()

    @classmethod
    def get_tile_maximum_variation(cls, _id):
        """..."""
        try:
            return cls.tiles[_id][TILE_W, 'default']['var']
        except KeyError:
            return 0

    @classmethod
    def get_tile(cls, _id, color=None,
                 tiling_index=0, tile_variation=0):
        """..."""
        if isinstance(_id, str):
            _id = ord(_id)

        try:
            surface = cls.tiles[_id][TILE_W, 'default']['img']
            col = tiling_index
            row = tile_variation
            src = col * TILE_W, row * TILE_H, TILE_W, TILE_H
        except KeyError:
            y = _id // (cls.tileset_width // TILE_W)
            x = _id % (cls.tileset_width // TILE_W)
            src = x * TILE_W, y * TILE_H, TILE_W, TILE_H
            surface = cls.get_set(color)

        return src, surface

    @classmethod
    def get_set(cls, color=None):
        """..."""
        __colors = 64
        __factor = 256 // __colors
        if color:
            color = tuple(c // __factor * __factor for c in (color))

        if color not in cls._tilesets:
            if color is None:
                cls._tilesets[color] = Images.get(TILESET)
            else:
                tileset = cls.color_surface(cls._tilesets[None], color)
                cls._tilesets[color] = tileset

        return cls._tilesets[color]

    @classmethod
    def color_surface(cls, surface, color):
        """..."""
        new_surface = surface.copy()
        arr = pygame.surfarray.pixels3d(new_surface)
        arr[:, :, 0] = color[0]
        arr[:, :, 1] = color[1]
        arr[:, :, 2] = color[2]
        del arr
        return new_surface

    def __getstate__(self):
        """..."""
        return None


class Fonts(Resources):
    """..."""

    @classmethod
    def __init__(cls, path=os.path.join(BASE_PATH, "fonts"), types=None):
        """..."""
        types = types if types else ['*.ttf']
        super().__init__(
            loader=pygame.font.Font,
            path=path,
            types=types,
            weak_ref=False)

    """
    @classmethod
    def _index(cls, path, types):
        _names = super()._index(path, types)
        print(_names)
        return _names
    """

    @classmethod
    def __getattr__(cls, name, size):
        """..."""
        try:
            font = cls.cache[name, size]
        except KeyError:
            # print("Loading font", cls._names[name])
            font = cls.loader(cls._names[name], size)
            cls.cache[name, size] = font
        return font

    @classmethod
    def load(cls, name, size):
        """..."""
        return cls.__getattr__(name, size)

    def __getstate__(self):
        """..."""
        return None
