"""..."""

import os
import sys
import weakref

import sdl2
import sdl2.ext

BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "resources")


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


class Fonts(Resources):
    """..."""

    @classmethod
    def __init__(
        cls, factory, path=os.path.join(BASE_PATH, "fonts"), types=None
    ):
        """..."""
        types = types or ['*.ttf']
        cls.factory = factory
        cls.font_manager = sdl2.ext.FontManager(
            font_path=path, alias="caladea-regular", size=12)
        super().__init__(
            loader=cls.font_manager.add,
            path=path,
            types=types,
            weak_ref=False)

    @classmethod
    def load(cls, name, size):
        """..."""
        alias = os.path.splitext(name)[0]
        try:
            cls.font_manager.fonts[alias][size]
        except KeyError:
            cls.loader(font_path=cls._names[name],
                       alias=os.path.splitext(name)[0],
                       size=size)

    @classmethod
    def render(cls, text, name, size, color):
        """..."""
        cls.load(name, size)
        print(text)

        sfc = cls.font_manager.render(text=text, size=size, color=color,
                                      alias=os.path.splitext(name)[0])
        return cls.factory.from_surface(sfc, True)

    @classmethod
    def text_size(cls, text, name, size):
        """..."""
        cls.load(name, size)
        return cls.font_manager.text_size(text, name, size)


    def __getstate__(self):
        """..."""
        return None
