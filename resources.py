import sys
import os

import pygame
import weakref


from constants import TILESET


class Tileset(object):
    cache = {}

    @classmethod
    def get(cls, color):
        if not hasattr(cls, 'tileset'):
            cls.tileset = pygame.image.load(
                os.path.join("resources", TILESET)).convert_alpha()
        if color is None:
            return cls.tileset
        else:
            try:
                tileset = cls.cache[color]
            except KeyError:
                tileset = cls.color_surface(cls.tileset, color)
                cls.cache[color] = tileset
            return tileset

    @classmethod
    def color_surface(cls, surface, color):
        new_surface = surface.copy()
        arr = pygame.surfarray.pixels3d(new_surface)
        arr[:, :, 0] = color[0]
        arr[:, :, 1] = color[1]
        arr[:, :, 2] = color[2]
        return new_surface

    def __getstate__(self):
        return None


class Resources(object):

    _names = {}

    @classmethod
    def __init__(cls, loader, path, types, weak_ref=True):
        cls._index(path, types)
        if weakref:
            cls.cache = weakref.WeakValueDictionary()
        else:
            cls.cache = {}
        cls.loader = loader

    @classmethod
    def __getattr__(cls, name):
        try:
            img = cls.cache[name]
        except KeyError:
            img = cls.loader(cls._names[name])
            cls.cache[name] = img
        return img

    @classmethod
    def load(cls, name):
        return cls.__getattr__(name)

    @classmethod
    def _index(cls, path, types):
        if sys.version_info >= (3, 5):
            # Python version >=3.5 supports glob
            import glob
            for img_type in types:
                for filename in glob.iglob(
                    (path + '/**/' + img_type), recursive=True
                ):
                    f_base = os.path.basename(filename)
                    cls._names.update({f_base: filename})
        else:
            # Python version <=3.4
            import fnmatch

            for root, dirnames, filenames in os.walk(path):
                for img_type in types:
                    for f_base in fnmatch.filter(filenames, img_type):
                        filename = os.path.join(root, f_base)
                        cls._names.update({f_base: filename})

    def __getstate__(self):
        return None


class Images(Resources):
    @classmethod
    def __init__(cls, path=".", types=['*.jpg', '*.png', '*.bmp']):
        super().__init__(
            loader=pygame.image.load,
            path=path,
            types=types)

    def __getstate__(self):
        return None


class Fonts(Resources):
    @classmethod
    def __init__(cls, path=".", types=['*.ttf']):
        super().__init__(
            loader=pygame.font.Font,
            path=path,
            types=types,
            weak_ref=False)

    @classmethod
    def __getattr__(cls, name, size):
        try:
            font = cls.cache[name, size]
        except KeyError:
            font = cls.loader(cls._names[name], size)
            cls.cache[name, size] = font
        return font

    @classmethod
    def load(cls, name, size):
        return cls.__getattr__(name, size)

    def __getstate__(self):
        return None
