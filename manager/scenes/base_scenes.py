"""..."""

from abc import ABCMeta, abstractmethod

import pygame
import manager


class EntityBase(metaclass=ABCMeta):

    @property
    def game(self):
        """..."""
        return manager.Game._instance

    @property
    def screen(self):
        """..."""
        return self.game.screen


class SceneBase(EntityBase):
    """Basic scene of the game.

    New Scenes should be subclasses of SceneBase.
    """

    # If set to True the update will not be called by Game.
    # Useful for cases where the scene needs to handle itself.
    ignore_regular_update = False

    @abstractmethod
    def __init__(self):
        """Implemented by subclasses."""
        pass

    @property
    def fonts(self):
        """..."""
        return self.game.fonts

    @property
    def width(self):
        """..."""
        if not hasattr(self, '_width'):
            self._width = self.screen.get_width()
        return self._width

    @width.setter
    def width(self, value):
        """..."""
        self._width = value

    @property
    def height(self):
        """..."""
        if not hasattr(self, '_height'):
            self._height = self.screen.get_height()
        return self._height

    @height.setter
    def height(self, value):
        """..."""
        self._height = value

    def start(self):
        """..."""
        pass

    def clear(self):
        """..."""
        pass

    def on_update(self):
        """Contain base scene logic.

        It is called from Game at every cycle.

        Should be overwritten on subclasses.
        """
        pass

    def post_update(self):
        """..."""
        pass

    def on_event(self, event):
        """Called when a specific event is detected in the loop.

        Deliver those events to their specific handlers.
        """
        if event.type == pygame.KEYDOWN:
            # print('key pressed')
            self.on_key_press(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button <= 3:
                self.on_mouse_press(event)
            else:
                self.on_mouse_scroll(event)

    def on_mouse_press(self, event):
        """Called when mouse buttons 1 or 2 are pressed."""
        pass

    def on_mouse_scroll(self, event):
        """Called when the mouse wheel is scrolled."""
        pass

    def on_key_press(self, event):
        """Called on keyboard input."""
        pass

    def on_key_held(self):
        """..."""
        pass

    def quit(self):
        """..."""
        self.game.alive = False

    def __getstate__(self):
        """..."""
        return None


class SceneMultiLayer(SceneBase):
    """..."""

    def __init__(self, draw_all=False):
        """..."""
        self.draw_all = draw_all
        self.layers = []

    def insert_layer(self, obj):
        self.layers.append(obj)

    def remove_layer(self, obj):
        self.layers.remove(obj)

    def on_update(self):
        """..."""
        if self.draw_all:
            for layer in self.layers:
                layer.on_update()
        else:
            if self.layers:
                self.layers[-1].on_update()

    def post_update(self):
        """..."""
        if self.draw_all:
            for layer in self.layers:
                layer.post_update()
        else:
            if self.layers:
                self.layers[-1].post_update()

    def on_key_press(self, event):
        """..."""
        if self.layers:
            self.layers[-1].on_key_press(event)


