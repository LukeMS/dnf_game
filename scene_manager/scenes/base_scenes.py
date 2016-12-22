"""..."""

import sdl2

from dnf_game.scene_manager.manager import Manager
from dnf_game.scene_manager.layers.base_layers import Hud
from dnf_game.scene_manager.base_entity import EntityBase


class SceneBase(EntityBase):
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
        if not isinstance(_manager, Manager):
            raise TypeError("_manager must be a Manager")
        scene = object.__new__(cls)
        scene.manager = _manager
        return scene

    def __init__(self, **kwargs):
        """..."""
        self._fps_hud = Hud(parent=self)

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

    def draw_fps(self, fps):
        """..."""
        self._fps_hud.text = fps
        self._fps_hud.draw()

    def on_key_release(self, event, mod):
        """Called on keyboard input, when a key is released."""
        # print("SceneBase.on_key_press")
        if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
            self.quit()

    def quit(self):
        """..."""
        # print("SceneBase.quit")
        self.manager.alive = False

    def __getstate__(self):
        """Prevent pickling by returning None."""
        return None


class SceneMultiLayer(SceneBase):
    """..."""

    def __init__(self, *, draw_all=False, **kwargs):
        """..."""
        super().__init__(**kwargs)
        self.draw_all = draw_all
        self.layers = []

    def insert_layer(self, *args):
        """..."""
        self.layers.extend(args)

    def remove_layer(self, obj):
        """..."""
        self.layers.remove(obj)

    def on_update(self):
        """..."""
        if self.draw_all:
            [layer.on_update() for layer in self.layers if layer]
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

    def on_key_press(self, event, mod):
        """Called on keyboard input, when a key is held down."""
        if self.layers:
            self.layers[-1].on_key_press(event, mod)
