import sys
import os

import pygame
import weakref


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


class Images(Resources):
    @classmethod
    def __init__(cls, path=".", types=['*.jpg', '*.png', '*.bmp']):
        super().__init__(
            loader=pygame.image.load,
            path=path,
            types=types)


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
