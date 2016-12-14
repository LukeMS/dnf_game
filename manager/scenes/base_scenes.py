"""..."""

import sdl2

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import manager


class SceneBase(object):
    """Basic scene of the game.

    New Scenes should be subclasses of SceneBase.
    """

    # If set to True the update will not be called by Game.
    # Useful for cases where the scene needs to handle itself.
    ignore_regular_update = False

    def __new__(cls, _manager, **kwargs):
        """Create a new instance of a scene.

        A reference to the manager is stored before returning it.
        """
        if not isinstance(_manager, manager.Manager):
            raise TypeError("_manager must be a Manager")
        scene = object.__new__(cls)
        scene.manager = _manager
        return scene

    def __init__(self, **kwargs):
        """..."""
        pass

    @property
    def fonts(self):
        """..."""
        return self.manager.fonts

    @property
    def factory(self):
        """..."""
        return self.manager.factory

    @property
    def width(self):
        """..."""
        return self.manager.width

    @property
    def height(self):
        """..."""
        return self.manager.height

    def start(self):
        """..."""
        pass

    def clear(self):
        """..."""
        pass

    def on_update(self):
        """Logic for graphics.

        Manager calls on_update on the active scene at every cycle.
        """
        pass

    def post_update(self):
        """..."""
        pass

    def on_event(self, event):
        """Called when a specific event is detected in the loop.

        Each event is delivered to their specific method.
        """
        # print("SceneBase.on_event")
        if event.type == sdl2.SDL_KEYDOWN:
            self.on_key_press(event)
        elif event.type == sdl2.SDL_MOUSEWHEEL:
                # event.wheel.y
                self.on_mouse_scroll(event)
        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            self.on_mouse_press(event)

    def on_mouse_press(self, event):
        """Called when mouse buttons pressed."""
        pass

    def on_mouse_scroll(self, event):
        """Called when the mouse wheel is scrolled."""
        pass

    def on_key_press(self, event):
        """Called on keyboard input."""
        # print("SceneBase.on_key_press")
        if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
            self.quit()

    def on_key_held(self):
        """..."""
        pass

    def quit(self):
        """..."""
        # print("SceneBase.quit")
        self.manager.alive = False

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
        """..."""
        self.layers.append(obj)

    def remove_layer(self, obj):
        """..."""
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
