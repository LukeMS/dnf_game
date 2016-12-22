"""..."""

from abc import ABCMeta, abstractmethod
import inspect
import os


class EntityBase(metaclass=ABCMeta):
    """Abstract entity inherited from both SceneBase an WindowBase."""

    @abstractmethod
    def __init__(self, **kwargs):
        """..."""
        pass

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        pass

    def on_key_release(self, event, mod):
        """Called on keyboard input, when a key is released."""
        pass

    def on_mouse_drag(self, x, y, dx, dy, button):
        """Called when mouse buttons are pressed and the mouse is dragged."""
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse is moved."""
        pass

    def on_mouse_press(self, event, x, y, button, double):
        """Called when mouse buttons are pressed."""
        pass

    def on_mouse_scroll(self, event, offset_x, offset_y):
        """Called when the mouse wheel is scrolled."""
        pass

    def on_update(self):
        """Graphical logic."""
        pass

    def post_update(self):
        """..."""
        pass

    def __repr__(self):
        """..."""
        return self.__str__()

    def __str__(self):
        """..."""
        path = inspect.getfile(self.__class__)
        f = os.path.basename(path)
        return "(%s:%s)" % (f, self.__class__.__name__)
