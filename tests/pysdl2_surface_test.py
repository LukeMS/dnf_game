"""Test Scene for manager using pysdl2."""

import unittest

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes
from dnf_game.util.ext import gfxdraw
from dnf_game.util.ext.rect import Rect


class PySDL2TextTest(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=ScenePySDL2TextTest, test=False).execute()


class ScenePySDL2TextTest(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        rect = Rect(50, 50, 200, 50)
        color = (255, 0, 0, 255)
        surface = self.factory.create_surface(rect.w, rect.h)
        gfxdraw.hlineRGBA(surface, 0, 50, 25, color,
                          sdlgfx="sfc")

        self.sprite = self.factory.from_surface(surface)

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.sprite)


if __name__ == '__main__':
    unittest.main(verbosity=2)
