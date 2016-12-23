"""Test Scene for manager using pysdl2."""

import unittest

from dnf_game.scene_manager import Manager
from dnf_game.scene_manager.scenes import base_scenes
from dnf_game.util.ext.rect import Rect


class GradientSpriteTestPySDL2(unittest.TestCase):
    """..."""

    def setUp(self):
        """..."""
        print("\n", "#" * 30, "\n%s" % __file__)

    def test_scene(self):
        """..."""
        Manager(scene=SceneGradientSpriteTestPySDL2, test=True).execute()


class SceneGradientSpriteTestPySDL2(base_scenes.SceneBase):
    """..."""

    def __init__(self, **kwargs):
        """..."""
        super().__init__(**kwargs)
        from_gradient = self.manager.factory.from_gradient
        self.sprite = from_gradient(color_start=(10, 36, 106, 0),
                                    color_end=(166, 202, 240, 0),
                                    rect=Rect(0, 0, 320, 240),
                                    mode="v")

    def on_update(self):
        """..."""
        self.manager.spriterenderer.render(sprites=self.sprite)


if __name__ == '__main__':
    unittest.main(verbosity=2)
