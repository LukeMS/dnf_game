"""..."""

import sys
import os
import random

import pygame
import weakref

from constants import TILESET, TILE_W, TILE_H


class Resources(object):
    """..."""

    _names = {}

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
            img = cls.cache[name]
        except KeyError:
            img = cls.loader(cls._names[name])
            cls.cache[name] = img
        return img

    @classmethod
    def load(cls, name):
        """..."""
        return cls.__getattr__(name)

    @classmethod
    def _index(cls, path, types):
        """..."""
        _names = {}
        if sys.version_info >= (3, 5):
            # Python version >=3.5 supports glob
            import glob
            for img_type in types:
                for filename in glob.iglob(
                    (path + '/**/' + img_type), recursive=True
                ):
                    f_base = os.path.basename(filename)
                    _names.update({f_base: filename})
        else:
            # Python version <=3.4
            import fnmatch

            for root, dirnames, filenames in os.walk(path):
                for img_type in types:
                    for f_base in fnmatch.filter(filenames, img_type):
                        filename = os.path.join(root, f_base)
                        _names.update({f_base: filename})
        return _names

    def __getstate__(self):
        """..."""
        return None


class Images(Resources):
    """..."""

    @classmethod
    def __init__(cls, path=".", types=['*.jpg', '*.png', '*.bmp']):
        """..."""
        super().__init__(
            loader=pygame.image.load,
            path=path,
            types=types)

    @classmethod
    def __getattr__(cls, name):
        """..."""
        try:
            img = cls.cache[name]
        except KeyError:
            img = cls.loader(cls._names[name]).convert_alpha()
            cls.cache[name] = img
        return img


class Tilesets(Images):
    """..."""

    _tilesets = {}

    @classmethod
    def __init__(cls, path=os.path.join("resources", "tilesets"),
                 types=['*.jpg', '*.png', '*.bmp']):
        """..."""
        cls.loader = pygame.image.load
        cls._names = cls._index(path=path, types=types)

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
                    'img': cls.load(k)
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
                cls._tilesets[color] = Images.load(TILESET)
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
    def __init__(cls, path=os.path.join("resources", "fonts"),
                 types=['*.ttf']):
        """..."""
        super().__init__(
            loader=pygame.font.Font,
            path=path,
            types=types,
            weak_ref=False)

    @classmethod
    def __getattr__(cls, name, size):
        """..."""
        try:
            font = cls.cache[name, size]
        except KeyError:
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
