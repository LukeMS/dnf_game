"""..."""

from ctypes import c_int, pointer


class Reference(object):
    """..."""

    def __init__(self, obj):
        """..."""
        self._obj = obj

    def __add__(self, other):
        """Implement addition."""
        self._obj = self._obj.__add__(other)

    def __str__(self):
        """Behavior for when str() is called this class."""
        return "Reference (%s) -> %s" % (hex(id(self._obj)),
                                         self._obj.__str__())

x = c_int(42)
y = pointer(5)

y.contents += 1

print(x)
