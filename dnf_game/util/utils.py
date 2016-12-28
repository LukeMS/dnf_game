"""Utility classes and methods used by various parts of the game."""
"""..."""

import os
from itertools import cycle, islice
import heapq

import dnf_game


def describe_error(e, info=None, dict_data=None):
    from pprint import pformat
    info = str(info) or " "
    arg_zero = str(e.args[0]) or " "
    if isinstance(e, (KeyError)):
        e.args = (">key = ", arg_zero, "; >info=%s" % info,
                  "; >data = ", dict_data)
    else:
        dict_data = pformat(dict_data, indent=4)
        info = arg_zero + ";\n" + info + ";\n" + dict_data
        e.args = (info, *e.args[1:])

if __name__ == '__main__':
    class F:
        def __init__(self):
            self.a = "a"
            self.b = "b"
            self.c = {**self.__dict__}

    f = F()
    try:
        f.d
    except AttributeError as e:
        info = "This is a custom AttributeError description"
        describe_error(e, info, f.__dict__)
        raise
    try:
        f.c["c"]
    except KeyError as e:
        info = "This is a custom KeyError description"
        describe_error(e, info, f.__dict__)
        raise


class SingletonMeta(type):
    """Restrict the instantiation of each class to one object.

    Must be declared as a metaclass of the singleton classes.

    Example:
        class SingletonJR(metaclass=Singleton)
            pass
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """..."""
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]


def dnf_path(*args):
    """Get the dnf_game base path."""
    return os.path.join(os.path.dirname(dnf_game.__file__), *args)


class Font(object):
    """..."""

    def __init__(self, *, renderer, name=None, font_size=None, color=None):
        """..."""
        self.renderer = renderer
        self.name = name or 'caladea-regular.ttf'
        self.font_size = font_size or 16
        self.color = color or (255, 255, 255, 255)

    @property
    def height(self):
        """..."""
        return self.get_height()

    @property
    def width(self):
        """..."""
        return self.get_width()

    @property
    def size(self):
        """..."""
        return self.get_size()

    def render(self, text, color=None, rect=None):
        """..."""
        color = color or self.color
        return self.renderer.render(
            text, self.name, self.font_size, color, rect)

    def render_w(self, text, wrap, color=None):
        """..."""
        color = color or self.color
        return self.renderer.render_w(
            text=text, name=self.name, size=self.font_size, color=color,
            wrap=wrap)

    def get_size(self, text=None):
        """..."""
        text = text or "A"
        w, h = self.renderer.text_size(text, self.name, self.font_size)
        return w, h

    def get_width(self, text=None):
        """..."""
        return self.get_size(text)[0]

    def get_height(self, text=None):
        """..."""
        return self.get_size(text)[1]


def flatten(*args):
    """..."""
    if len(args) == 1:
        return args[0]
    else:
        return args


class RangedDictionary(dict):
    """..."""

    def __getitem__(self, key):
        """..."""
        for rng in self.keys():
            if key == rng:
                return super().__getitem__(key)
            if key in rng:
                return super().__getitem__(rng)
        return super().__getitem__(key)


class LBPercentTable(object):
    """A table of values with lower boundaries range indexes.

    Usage:
        table = (
            (0, "red"),
            (25, "yellow"),
            (50, "lime"),
            (75, "green")
        )

        lb_t = LBPercentTable(table, True)

        assert lb_t.get(-24) == "red"
        assert lb_t.get(50) == "lime"
        assert lb_t.get(999) == "green"
    """

    def __init__(self, table, default_to_first=False):
        """Initialization.

        Args:
            table (list, tuple): a list or tuple containing two-tuples (index,
            value)
            default_to_first: defaults to False. When False, values smaller
            then the first entry will return None. If True, the first entry
            value will be returned.

        Usage:
            table = (
                (0, "red"),
                (25, "yellow"),
                (50, "lime"),
                (75, "green")
            )
            lb_t = LBPercentTable(table, True)
        """
        self.default_to_first = default_to_first
        self.table = table

    def get(self, key):
        """Return a value of the table, according to the passed key.

        Args:
            key (*): the key to be searched on the table

        Returns:
            *: the proper table entry value for the key

        Usage:
            lb_t.get(50)
        """
        for (lb, v) in reversed(self.table):
            if key >= lb:
                return v
        return v if self.default_to_first else None


class PriorityQueue:
    """..."""

    def __init__(self):
        """..."""
        self.elements = []

    def empty(self):
        """..."""
        return len(self.elements) == 0

    def put(self, item, priority):
        """..."""
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        """..."""
        return heapq.heappop(self.elements)[1]


def roundrobin(*iterables):
    """Create a new iterable from merging two or more objects.

    Recipe credited to George Sakkis

    Usage:
        roundrobin('ABC', 'D', 'EF') --> A D E B F C
    """
    pending = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


def get_mod_case(event):
    """Check the state of the shift and caps lock keys.

    Switches the case of the s string if needed.

    Adapted from: http://inventwithpython.com/extra/gorillas.py
    """
    s = chr(event.key.keysym.sym)
    mod = event.mod
    if (bool(mod & pygame.KMOD_RSHIFT or mod & pygame.KMOD_LSHIFT) ^
            bool(mod & pygame.KMOD_CAPS)):
        return s.swapcase()
    else:
        return s


def shoehorn(s):
    """Remove accents (but also other things, like ß‘’“”)."""
    import unicodedata as ud
    return ud.normalize('NFKD', s).encode(
        'ascii', 'ignore').decode('utf-8', 'ignore')



class CustomSet(set):
    """..."""

    def append(self, item):
        """Enable list method append on sets."""
        self.add(item)


class Position:
    """..."""

    def __init__(self, pos):
        """..."""
        self.x, self.y = pos

    @property
    def pos(self):
        """..."""
        return (self.x, self.y)

    def __mod__(self, n):
        """..."""
        try:
            return Position((self.x % n[0], self.y % n[1]))
        except TypeError:
            return Position((self.x % n, self.y % n))

    def __truediv__(self, n):
        """..."""
        try:
            return Position((self.x / n[0], self.y / n[1]))
        except TypeError:
            return Position((self.x / n, self.y / n))

    def __mul__(self, n):
        """..."""
        try:
            return Position((self.x * n[0], self.y * n[1]))
        except TypeError:
            return Position((self.x * n, self.y * n))

    def __floordiv__(self, n):
        """..."""
        try:
            return Position((self.x // n[0], self.y // n[1]))
        except TypeError:
            return Position((self.x // n, self.y // n))

    def __add__(self, n):
        """..."""
        if n:
            try:
                return Position((self.x + n[0], self.y + n[1]))
            except TypeError:
                return Position((self.x + n, self.y + n))
    """
    def __add__(self, n):
        try:
            return Position((self.x + n[0], self.y + n[1]))
        except TypeError:
            try:
                return Position((self.x + n, self.y + n))
            except TypeError:
                if n is None:
                    return self.pos
    """

    def __sub__(self, n):
        """..."""
        try:
            return Position((self.x - n[0], self.y - n[1]))
        except TypeError:
            return Position((self.x - n, self.y - n))

    def __eq__(self, n):
        """..."""
        try:
            return (self.x, self.y) == n
        except TypeError:
            return self.x == n.x and self.y == n.y

    def __iter__(self):
        """..."""
        return iter((self.x, self.y))

    def __hash__(self):
        """..."""
        return hash((self.x, self.y))

    def __repr__(self):
        """..."""
        return (self.__class__.__name__ +
                "(({x}, {y}))".format(x=self.x, y=self.y))

    def __str__(self):
        """..."""
        return (self.__class__.__name__ +
                "[x={x}, y={y}]".format(x=self.x, y=self.y))

    def __getitem__(self, key):
        """..."""
        return self.pos[key]

class classproperty:
    """
    Same as property(), but passes obj.__class__ instead of obj to fget/fset/fdel.
    Original code for property emulation:
    https://docs.python.org/3.5/howto/descriptor.html#properties
    """
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj.__class__)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj.__class__, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj.__class__)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


def classproperty_support(cls):
    """
    Class decorator to add metaclass to our class.
    Metaclass uses to add descriptors to class attributes, see:
    http://stackoverflow.com/a/26634248/1113207
    """
    class Meta(type):
        pass

    for name, obj in vars(cls).items():
        if isinstance(obj, classproperty):
            setattr(Meta, name, property(obj.fget, obj.fset, obj.fdel))

    class Wrapper(cls, metaclass=Meta):
        pass
    return Wrapper

