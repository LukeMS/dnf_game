"""..."""

import sdl2

from dnf_game.scene_manager.layers.base_layers import Hud
from dnf_game.scene_manager.base_entity import (
    EntityBase, MultiLayeredEntityBase)


class SceneBase(EntityBase):
    """Basic scene of the game.

    New Scenes should be subclasses of SceneBase.
    """

    # If set to True the update will not be called by Game.
    # Useful for cases where the scene needs to handle itself.
    ignore_regular_update = False

    def __new__(cls, manager, **kwargs):
        """Create a new instance of a scene.

        A reference to the manager is stored before returning it.

        Args:
            manager (dnf_game.scene_manager.manager.Manager): a instance
            of the Manager
        """
        scene = super().__new__(cls)
        scene.manager = manager
        return scene

    def __init__(self, **kwargs):
        """Initialization."""
        self._fps_hud = Hud(parent=self)

    @property
    def width(self):
        """Main window width."""
        return self.manager.width

    @property
    def height(self):
        """Main window height."""
        return self.manager.height

    def draw_fps(self, fps):
        """Draw the FPS display when called by the Manager."""
        self._fps_hud.text = fps
        self._fps_hud.on_update()

    def on_key_release(self, event, mod):
        """super__doc__."""
        if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
            self.quit()

    def quit(self):
        """Stop the manager main loop."""
        self.manager.alive = False


class SceneMultiLayer(MultiLayeredEntityBase, SceneBase):
    """Scene with child entities (e.g.:layers)."""

    def __init__(self, *, draw_all=True, **kwargs):
        """Initialization."""
        SceneBase.__init__(self, **kwargs)
        MultiLayeredEntityBase.__init__(self, draw_all=draw_all, **kwargs)

    def on_key_release(self, event, mod):
        """super__doc__."""
        if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
            self.quit()
        super().on_key_release(event=event, mod=mod)
